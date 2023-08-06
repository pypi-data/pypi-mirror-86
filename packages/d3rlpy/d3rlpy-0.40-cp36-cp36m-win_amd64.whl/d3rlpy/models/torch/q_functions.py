import torch
import torch.nn as nn
import torch.nn.functional as F
import math

from abc import ABCMeta, abstractmethod


def create_discrete_q_function(observation_shape,
                               action_size,
                               encoder_factory,
                               n_ensembles=1,
                               n_quantiles=32,
                               embed_size=64,
                               q_func_type='mean',
                               bootstrap=False,
                               share_encoder=False):

    if share_encoder:
        encoder = encoder_factory.create(observation_shape)
        # normalize gradient scale by ensemble size
        for p in encoder.parameters():
            p.register_hook(lambda grad: grad / n_ensembles)

    q_funcs = []
    for _ in range(n_ensembles):
        if not share_encoder:
            encoder = encoder_factory.create(observation_shape)
        if q_func_type == 'mean':
            q_func = DiscreteQFunction(encoder, action_size)
        elif q_func_type == 'qr':
            q_func = DiscreteQRQFunction(encoder, action_size, n_quantiles)
        elif q_func_type == 'iqn':
            q_func = DiscreteIQNQFunction(encoder, action_size, n_quantiles,
                                          embed_size)
        elif q_func_type == 'fqf':
            q_func = DiscreteFQFQFunction(encoder, action_size, n_quantiles,
                                          embed_size)
        else:
            raise ValueError('invalid quantile regression type')
        q_funcs.append(q_func)
    return EnsembleDiscreteQFunction(q_funcs, bootstrap)


def create_continuous_q_function(observation_shape,
                                 action_size,
                                 encoder_factory,
                                 n_ensembles=1,
                                 n_quantiles=32,
                                 embed_size=64,
                                 q_func_type='mean',
                                 bootstrap=False,
                                 share_encoder=False):

    if share_encoder:
        encoder = encoder_factory.create(observation_shape, action_size)
        # normalize gradient scale by ensemble size
        for p in encoder.parameters():
            p.register_hook(lambda grad: grad / n_ensembles)

    q_funcs = []
    for _ in range(n_ensembles):
        if not share_encoder:
            encoder = encoder_factory.create(observation_shape, action_size)
        if q_func_type == 'mean':
            q_func = ContinuousQFunction(encoder)
        elif q_func_type == 'qr':
            q_func = ContinuousQRQFunction(encoder, n_quantiles)
        elif q_func_type == 'iqn':
            q_func = ContinuousIQNQFunction(encoder, n_quantiles, embed_size)
        elif q_func_type == 'fqf':
            q_func = ContinuousFQFQFunction(encoder, n_quantiles, embed_size)
        else:
            raise ValueError('invalid quantile regression type')
        q_funcs.append(q_func)
    return EnsembleContinuousQFunction(q_funcs, bootstrap)


def _pick_value_by_action(values, action, keepdims=False):
    action_size = values.shape[1]
    one_hot = F.one_hot(action.view(-1), num_classes=action_size)
    # take care of 3 dimensional vectors
    if values.ndim == 3:
        one_hot = one_hot.view(-1, action_size, 1)
    masked_values = values * one_hot.float()
    return masked_values.sum(dim=1, keepdims=keepdims)


def _huber_loss(y, target, beta=1.0):
    diff = target - y
    cond = diff.detach().abs() < beta
    return torch.where(cond, 0.5 * diff**2, beta * (diff.abs() - 0.5 * beta))


def _quantile_huber_loss(y, target, taus):
    assert y.ndim == 3
    assert target.ndim == 3
    assert taus.ndim == 3
    # compute huber loss
    huber_loss = _huber_loss(y, target)
    delta = ((target - y).detach() < 0.0).float()
    element_wise_loss = ((taus - delta).abs() * huber_loss)
    return element_wise_loss.sum(dim=2).mean(dim=1)


def _make_taus_prime(n_quantiles, device):
    steps = torch.arange(n_quantiles, dtype=torch.float32, device=device)
    taus = ((steps + 1).float() / n_quantiles).view(1, -1)
    taus_dot = (steps.float() / n_quantiles).view(1, -1)
    return (taus + taus_dot) / 2.0


def _reduce(value, reduction_type):
    if reduction_type == 'mean':
        return value.mean()
    elif reduction_type == 'sum':
        return value.sum()
    elif reduction_type == 'none':
        return value.view(-1, 1)
    raise ValueError('invalid reduction type.')


class QFunction(metaclass=ABCMeta):
    @abstractmethod
    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        pass

    @abstractmethod
    def compute_target(self, x, action):
        pass


class DiscreteQRQFunction(QFunction, nn.Module):
    def __init__(self, encoder, action_size, n_quantiles):
        super().__init__()
        self.encoder = encoder
        self.action_size = action_size
        self.n_quantiles = n_quantiles
        self.fc = nn.Linear(encoder.get_feature_size(),
                            action_size * n_quantiles)

    def forward(self, x, as_quantiles=False):
        h = self.encoder(x)
        quantiles = self.fc(h).view(-1, self.action_size, self.n_quantiles)

        if as_quantiles:
            return quantiles

        return quantiles.mean(dim=2)

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        assert q_tp1.shape == (obs_t.shape[0], self.n_quantiles)

        # extraect quantiles corresponding to act_t
        quantiles_t = _pick_value_by_action(self.forward(obs_t, True), act_t)

        # prepare taus for probabilities
        taus = _make_taus_prime(self.n_quantiles, obs_t.device)

        # compute quantile huber loss
        y = (rew_tp1 + gamma * q_tp1).view(obs_t.shape[0], -1, 1)
        quantiles_t = quantiles_t.view(obs_t.shape[0], 1, -1)
        taus = taus.view(1, 1, -1)
        loss = _quantile_huber_loss(quantiles_t, y, taus)

        return _reduce(loss, reduction)

    def compute_target(self, x, action=None):
        if action is None:
            return self.forward(x, True)
        return _pick_value_by_action(self.forward(x, True), action)


class ContinuousQRQFunction(QFunction, nn.Module):
    def __init__(self, encoder, n_quantiles):
        super().__init__()
        self.encoder = encoder
        self.action_size = encoder.action_size
        self.n_quantiles = n_quantiles
        self.fc = nn.Linear(encoder.get_feature_size(), n_quantiles)

    def forward(self, x, action, as_quantiles=False):
        h = self.encoder(x, action)
        quantiles = self.fc(h)

        if as_quantiles:
            return quantiles

        return quantiles.mean(dim=1, keepdims=True)

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        assert q_tp1.shape == (obs_t.shape[0], self.n_quantiles)

        quantiles_t = self.forward(obs_t, act_t, as_quantiles=True)

        # prepare taus for probabilities
        taus = _make_taus_prime(self.n_quantiles, obs_t.device)

        # compute quantile huber loss
        y = (rew_tp1 + gamma * q_tp1).view(obs_t.shape[0], -1, 1)
        quantiles_t = quantiles_t.view(obs_t.shape[0], 1, -1)
        taus = taus.view(1, 1, -1)
        loss = _quantile_huber_loss(quantiles_t, y, taus)

        return _reduce(loss, reduction)

    def compute_target(self, x, action):
        return self.forward(x, action, as_quantiles=True)


class DiscreteIQNQFunction(QFunction, nn.Module):
    def __init__(self, encoder, action_size, n_quantiles, embed_size):
        super().__init__()
        self.encoder = encoder
        self.action_size = action_size
        self.embed_size = embed_size
        self.n_quantiles = n_quantiles
        self.embed = nn.Linear(embed_size, encoder.get_feature_size())
        self.fc = nn.Linear(encoder.get_feature_size(), self.action_size)

    def _make_taus(self, h):
        taus = torch.rand(h.shape[0], self.n_quantiles, device=h.device)
        return taus

    def _compute_quantiles(self, h, taus):
        # compute embedding
        steps = torch.arange(self.embed_size, device=h.device).float() + 1
        # (batch, quantile, embedding)
        expanded_taus = taus.view(h.shape[0], self.n_quantiles, 1)
        prior = torch.cos(math.pi * steps.view(1, 1, -1) * expanded_taus)
        # (batch, quantile, embedding) -> (batch, quantile, feature)
        phi = torch.relu(self.embed(prior))

        # (batch, 1, feature) -> (batch,  quantile, feature)
        prod = h.view(h.shape[0], 1, -1) * phi

        # (batch, quantile, feature) -> (batch, action, quantile)
        return self.fc(prod).transpose(1, 2)

    def forward(self, x, as_quantiles=False, with_taus=False):
        h = self.encoder(x)

        taus = self._make_taus(h)

        quantiles = self._compute_quantiles(h, taus)

        rets = []

        if as_quantiles:
            rets.append(quantiles)
        else:
            rets.append(quantiles.mean(dim=2))

        if with_taus:
            rets.append(taus)

        if len(rets) == 1:
            return rets[0]
        return rets

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        assert q_tp1.shape == (obs_t.shape[0], self.n_quantiles)

        # extraect quantiles corresponding to act_t
        values, taus = self.forward(obs_t, as_quantiles=True, with_taus=True)
        quantiles_t = _pick_value_by_action(values, act_t)

        # compute errors with all combination
        y = (rew_tp1 + gamma * q_tp1).view(obs_t.shape[0], -1, 1)
        quantiles_t = quantiles_t.view(obs_t.shape[0], 1, -1)
        taus = taus.view(obs_t.shape[0], 1, -1)
        loss = _quantile_huber_loss(quantiles_t, y, taus)

        return _reduce(loss, reduction)

    def compute_target(self, x, action=None):
        quantiles = self.forward(x, as_quantiles=True)
        if action is None:
            return quantiles
        return _pick_value_by_action(quantiles, action)


class ContinuousIQNQFunction(QFunction, nn.Module):
    def __init__(self, encoder, n_quantiles, embed_size):
        super().__init__()
        self.encoder = encoder
        self.action_size = encoder.action_size
        self.embed_size = embed_size
        self.n_quantiles = n_quantiles
        self.embed = nn.Linear(embed_size, encoder.get_feature_size())
        self.fc = nn.Linear(encoder.get_feature_size(), 1)

    def _make_taus(self, h):
        taus = torch.rand(h.shape[0], self.n_quantiles, device=h.device)
        return taus

    def _compute_quantiles(self, h, taus):
        # compute embedding
        steps = torch.arange(self.embed_size, device=h.device).float() + 1
        # (batch, quantile, embedding)
        expanded_taus = taus.view(h.shape[0], -1, 1)
        prior = torch.cos(math.pi * steps.view(1, 1, -1) * expanded_taus)
        # (batch, quantile, embedding) -> (batch, quantile, feature)
        phi = torch.relu(self.embed(prior))

        # (batch, 1, feature) -> (batch, quantile, feature)
        prod = h.view(h.shape[0], 1, -1) * phi

        # (batch, quantile, feature) -> (batch, quantile)
        quantiles = self.fc(prod).view(h.shape[0], -1)

        return quantiles

    def forward(self, x, action, as_quantiles=False, with_taus=False):
        h = self.encoder(x, action)

        taus = self._make_taus(h)

        quantiles = self._compute_quantiles(h, taus)

        rets = []

        if as_quantiles:
            rets.append(quantiles)
        else:
            rets.append(quantiles.mean(dim=1, keepdims=True))

        if with_taus:
            rets.append(taus)

        if len(rets) == 1:
            return rets[0]
        return rets

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        assert q_tp1.shape == (obs_t.shape[0], self.n_quantiles)

        quantiles_t, taus = self.forward(obs_t,
                                         act_t,
                                         as_quantiles=True,
                                         with_taus=True)

        # compute errors with all combination
        y = (rew_tp1 + gamma * q_tp1).view(obs_t.shape[0], -1, 1)
        quantiles_t = quantiles_t.view(obs_t.shape[0], 1, -1)
        taus = taus.view(obs_t.shape[0], 1, -1)
        loss = _quantile_huber_loss(quantiles_t, y, taus)

        return _reduce(loss, reduction)

    def compute_target(self, x, action):
        return self.forward(x, action, as_quantiles=True)


class DiscreteFQFQFunction(DiscreteIQNQFunction):
    def __init__(self, encoder, action_size, n_quantiles, embed_size):
        super().__init__(encoder, action_size, n_quantiles, embed_size)
        self.proposal = nn.Linear(encoder.get_feature_size(), n_quantiles)

    def _make_taus(self, h):
        # compute taus without making backward path
        proposals = self.proposal(h.detach())
        # tau_i+1
        log_probs = torch.log_softmax(proposals, dim=1)
        probs = log_probs.exp()
        taus = torch.cumsum(probs, dim=1)

        # tau_i
        pads = torch.zeros(h.shape[0], 1, device=h.device)
        taus_minus = torch.cat([pads, taus[:, :-1]], dim=1)

        # tau^
        taus_prime = (taus + taus_minus) / 2

        # entropy for penalty
        entropies = -(log_probs * probs).sum(dim=1)

        return taus, taus_minus, taus_prime, entropies

    def forward(self, x, as_quantiles=False, with_taus=False, with_h=False):
        h = self.encoder(x)

        taus, taus_minus, taus_prime, entropies = self._make_taus(h)

        # compute quantiles without making backward path to proposal net
        quantiles = self._compute_quantiles(h, taus_prime.detach())

        rets = []

        if as_quantiles:
            rets.append(quantiles)
        else:
            weight = (taus - taus_minus).view(-1, 1, self.n_quantiles).detach()
            rets.append((weight * quantiles).sum(dim=2))

        if with_taus:
            rets.append([taus, taus_prime, entropies])

        if with_h:
            rets.append(h)

        if len(rets) == 1:
            return rets[0]
        return rets

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        assert q_tp1.shape == (obs_t.shape[0], self.n_quantiles)

        # extraect quantiles corresponding to act_t
        values, taus, h = self.forward(obs_t,
                                       as_quantiles=True,
                                       with_taus=True,
                                       with_h=True)
        taus, taus_prime, entropies = taus

        quantiles_t = _pick_value_by_action(values, act_t)

        # compute errors with all combination
        y = (rew_tp1 + gamma * q_tp1).view(obs_t.shape[0], -1, 1)
        quantiles_t = quantiles_t.view(obs_t.shape[0], 1, -1)
        taus_prime = taus_prime.view(obs_t.shape[0], 1, -1).detach()
        quantile_loss = _quantile_huber_loss(quantiles_t, y, taus_prime)

        # compute proposal network loss
        # original paper explicitly separates the optimization process
        # but, it's combined here
        q_taus = self._compute_quantiles(h.detach(), taus)
        q_taus_prime = self._compute_quantiles(h.detach(), taus_prime)
        batch_steps = torch.arange(obs_t.shape[0])
        # (batch, n_quantiles - 1)
        q_taus = q_taus[batch_steps, act_t.view(-1)][:, :-1]
        # (batch, n_quantiles)
        q_taus_prime = q_taus_prime[batch_steps, act_t.view(-1)]

        # compute gradients
        proposal_grad = 2 * q_taus - q_taus_prime[:, :-1] - q_taus_prime[:, 1:]
        proposal_loss = (proposal_grad.detach() * taus[:, :-1]).sum(dim=1)

        # small learning rate for prpposal network
        loss = quantile_loss + 1e-5 * (proposal_loss - 1e-3 * entropies)

        return _reduce(loss, reduction)


class ContinuousFQFQFunction(ContinuousIQNQFunction):
    def __init__(self, encoder, n_quantiles, embed_size):
        super().__init__(encoder, n_quantiles, embed_size)
        self.proposal = nn.Linear(encoder.get_feature_size(), n_quantiles)

    def _make_taus(self, h):
        # compute taus without making backward path
        proposals = self.proposal(h.detach())
        # tau_i+1
        log_probs = torch.log_softmax(proposals, dim=1)
        probs = log_probs.exp()
        taus = torch.cumsum(probs, dim=1)

        # tau_i
        pads = torch.zeros(h.shape[0], 1, device=h.device)
        taus_minus = torch.cat([pads, taus[:, :-1]], dim=1)

        # tau^
        taus_prime = (taus + taus_minus) / 2

        # entropy for penalty
        entropies = -(log_probs * probs).sum(dim=1)

        return taus, taus_minus, taus_prime, entropies

    def forward(self,
                x,
                action,
                as_quantiles=False,
                with_taus=False,
                with_h=False):
        h = self.encoder(x, action)

        taus, taus_minus, taus_prime, entropies = self._make_taus(h)

        # compute quantiles without making backward path to proposal net
        quantiles = self._compute_quantiles(h, taus_prime.detach())

        rets = []

        if as_quantiles:
            rets.append(quantiles)
        else:
            weight = (taus - taus_minus).detach()
            rets.append((weight * quantiles).sum(dim=1, keepdims=True))

        if with_taus:
            rets.append([taus, taus_prime, entropies])

        if with_h:
            rets.append(h)

        if len(rets) == 1:
            return rets[0]
        return rets

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        assert q_tp1.shape == (obs_t.shape[0], self.n_quantiles)

        values, taus, h = self.forward(obs_t,
                                       act_t,
                                       as_quantiles=True,
                                       with_taus=True,
                                       with_h=True)
        taus, taus_prime, entropies = taus

        # compute errors with all combination
        y = (rew_tp1 + gamma * q_tp1).view(obs_t.shape[0], -1, 1)
        quantiles_t = values.view(obs_t.shape[0], 1, -1)
        taus_prime_t = taus_prime.view(obs_t.shape[0], 1, -1).detach()
        quantile_loss = _quantile_huber_loss(quantiles_t, y, taus_prime_t)

        # compute proposal network loss
        # original paper explicitly separates the optimization process
        # but, it's combined here
        # (batch, n_quantiles - 1)
        q_taus = self._compute_quantiles(h.detach(), taus)[:, :-1]
        # (batch, n_quantiles)
        q_taus_prime = self._compute_quantiles(h.detach(), taus_prime)

        # compute gradients
        proposal_grad = 2 * q_taus - q_taus_prime[:, :-1] - q_taus_prime[:, 1:]
        proposal_loss = (proposal_grad.detach() * taus[:, :-1]).sum(dim=1)

        # small lerarning rate for proposal network
        loss = quantile_loss + 1e-5 * (proposal_loss - 1e-3 * entropies)

        return _reduce(loss, reduction)


class DiscreteQFunction(QFunction, nn.Module):
    def __init__(self, encoder, action_size):
        super().__init__()
        self.action_size = action_size
        self.encoder = encoder
        self.fc = nn.Linear(encoder.get_feature_size(), action_size)

    def forward(self, x):
        h = self.encoder(x)
        return self.fc(h)

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        one_hot = F.one_hot(act_t.view(-1), num_classes=self.action_size)
        q_t = (self.forward(obs_t) * one_hot.float()).sum(dim=1, keepdims=True)
        y = rew_tp1 + gamma * q_tp1
        loss = _huber_loss(q_t, y)
        return _reduce(loss, reduction)

    def compute_target(self, x, action=None):
        if action is None:
            return self.forward(x)
        return _pick_value_by_action(self.forward(x), action, keepdims=True)


class ContinuousQFunction(QFunction, nn.Module):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder
        self.action_size = encoder.action_size
        self.fc = nn.Linear(encoder.get_feature_size(), 1)

    def forward(self, x, action):
        h = self.encoder(x, action)
        return self.fc(h)

    def compute_error(self,
                      obs_t,
                      act_t,
                      rew_tp1,
                      q_tp1,
                      gamma=0.99,
                      reduction='mean'):
        q_t = self.forward(obs_t, act_t)
        y = rew_tp1 + gamma * q_tp1
        loss = F.mse_loss(q_t, y, reduction='none')
        return _reduce(loss, reduction)

    def compute_target(self, x, action):
        return self.forward(x, action)


def _reduce_ensemble(y, reduction='min', dim=0, lam=0.75):
    if reduction == 'min':
        return y.min(dim=dim).values
    elif reduction == 'max':
        return y.max(dim=dim).values
    elif reduction == 'mean':
        return y.mean(dim=dim)
    elif reduction == 'none':
        return y
    elif reduction == 'mix':
        max_values = y.max(dim=dim).values
        min_values = y.min(dim=dim).values
        return lam * min_values + (1.0 - lam) * max_values
    raise ValueError


def _gather_quantiles_by_indices(y, indices):
    # TODO: implement this in general case
    if y.ndim == 3:
        # (N, batch, n_quantiles) -> (batch, n_quantiles)
        return y.transpose(0, 1)[torch.arange(y.shape[1]), indices]
    elif y.ndim == 4:
        # (N, batch, action, n_quantiles) -> (batch, action, N, n_quantiles)
        transposed_y = y.transpose(0, 1).transpose(1, 2)
        # (batch, action, N, n_quantiles) -> (batch * action, N, n_quantiles)
        flat_y = transposed_y.reshape(-1, y.shape[0], y.shape[3])
        head_indices = torch.arange(y.shape[1] * y.shape[2])
        # (batch * action, N, n_quantiles) -> (batch * action, n_quantiles)
        gathered_y = flat_y[head_indices, indices.view(-1)]
        # (batch * action, n_quantiles) -> (batch, action, n_quantiles)
        return gathered_y.view(y.shape[1], y.shape[2], -1)
    raise ValueError


def _reduce_quantile_ensemble(y, reduction='min', dim=0, lam=0.75):
    # reduction beased on expectation
    mean = y.mean(dim=-1)
    if reduction == 'min':
        indices = mean.min(dim=dim).indices
        return _gather_quantiles_by_indices(y, indices)
    elif reduction == 'max':
        indices = mean.max(dim=dim).indices
        return _gather_quantiles_by_indices(y, indices)
    elif reduction == 'none':
        return y
    elif reduction == 'mix':
        min_indices = mean.min(dim=dim).indices
        max_indices = mean.max(dim=dim).indices
        min_values = _gather_quantiles_by_indices(y, min_indices)
        max_values = _gather_quantiles_by_indices(y, max_indices)
        return lam * min_values + (1.0 - lam) * max_values
    raise ValueError


class EnsembleQFunction(nn.Module):
    def __init__(self, q_funcs, bootstrap=False):
        super().__init__()
        self.action_size = q_funcs[0].action_size
        self.q_funcs = nn.ModuleList(q_funcs)
        self.bootstrap = bootstrap and len(q_funcs) > 1

    def compute_error(self, obs_t, act_t, rew_tp1, q_tp1, gamma=0.99):
        td_sum = 0.0
        for i, q_func in enumerate(self.q_funcs):
            loss = q_func.compute_error(obs_t,
                                        act_t,
                                        rew_tp1,
                                        q_tp1,
                                        gamma,
                                        reduction='none')

            if self.bootstrap:
                mask = torch.randint(0, 2, loss.shape, device=obs_t.device)
                loss *= mask.float()

            td_sum += loss.mean()

        return td_sum

    def compute_target(self, x, action=None, reduction='min'):
        values = []
        for q_func in self.q_funcs:
            target = q_func.compute_target(x, action)
            values.append(target.reshape(1, x.shape[0], -1))

        values = torch.cat(values, dim=0)

        if action is None:
            # mean Q function
            if values.shape[2] == self.action_size:
                return _reduce_ensemble(values, reduction)
            # distributional Q function
            n_q_funcs = values.shape[0]
            values = values.view(n_q_funcs, x.shape[0], self.action_size, -1)
            return _reduce_quantile_ensemble(values, reduction)

        if values.shape[2] == 1:
            return _reduce_ensemble(values, reduction)

        return _reduce_quantile_ensemble(values, reduction)


class EnsembleDiscreteQFunction(EnsembleQFunction):
    def forward(self, x, reduction='mean'):
        values = []
        for q_func in self.q_funcs:
            values.append(q_func(x).view(1, x.shape[0], self.action_size))
        return _reduce_ensemble(torch.cat(values, dim=0), reduction)


class EnsembleContinuousQFunction(EnsembleQFunction):
    def forward(self, x, action, reduction='mean'):
        values = []
        for q_func in self.q_funcs:
            values.append(q_func(x, action).view(1, x.shape[0], 1))
        return _reduce_ensemble(torch.cat(values, dim=0), reduction)


def compute_max_with_n_actions(x,
                               actions,
                               q_func,
                               lam,
                               with_action_indices=False):
    """ Returns weighted target value from sampled actions.

    This calculation is proposed in BCQ paper for the first time.

    `x` should be shaped with `(batch, dim_obs)`.
    `actions` should be shaped with `(batch, N, dim_action)`.

    """
    batch_size = actions.shape[0]
    n_critics = len(q_func.q_funcs)
    n_actions = actions.shape[1]

    # (batch, observation) -> (batch, n, observation)
    expanded_x = x.expand(n_actions, *x.shape).transpose(0, 1)
    # (batch * n, observation)
    flat_x = expanded_x.reshape(-1, *x.shape[1:])
    # (batch, n, action) -> (batch * n, action)
    flat_actions = actions.reshape(batch_size * n_actions, -1)

    # estimate values while taking care of quantiles
    flat_values = q_func.compute_target(flat_x, flat_actions, 'none')
    # reshape to (n_ensembles, batch_size, n, -1)
    transposed_values = flat_values.view(n_critics, batch_size, n_actions, -1)
    # (n_ensembles, batch_size, n, -1) -> (batch_size, n_ensembles, n, -1)
    values = transposed_values.transpose(0, 1)

    # get combination indices
    # (batch_size, n_ensembles, n, -1) -> (batch_size, n_ensembles, n)
    mean_values = values.mean(dim=3)
    #(batch_size, n_ensembles, n) -> (batch_size, n)
    max_values, max_indices = mean_values.max(dim=1)
    min_values, min_indices = mean_values.min(dim=1)
    mix_values = (1.0 - lam) * max_values + lam * min_values
    #(batch_size, n) -> (batch_size,)
    action_indices = mix_values.argmax(dim=1)

    # fuse maximum values and minimum values
    # (batch_size, n_ensembles, n, -1) -> (batch_size, n, n_ensembles, -1)
    values_T = values.transpose(1, 2)
    # (batch, n, n_ensembles, -1) -> (batch * n, n_ensembles, -1)
    flat_values = values_T.reshape(batch_size * n_actions, n_critics, -1)
    # (batch * n, n_ensembles, -1) -> (batch * n, -1)
    bn_indices = torch.arange(batch_size * n_actions)
    max_values = flat_values[bn_indices, max_indices.view(-1)]
    min_values = flat_values[bn_indices, min_indices.view(-1)]
    # (batch * n, -1) -> (batch, n, -1)
    max_values = max_values.view(batch_size, n_actions, -1)
    min_values = min_values.view(batch_size, n_actions, -1)
    mix_values = (1.0 - lam) * max_values + lam * min_values
    # (batch, n, -1) -> (batch, -1)
    result_values = mix_values[torch.arange(x.shape[0]), action_indices]

    if with_action_indices:
        return result_values, action_indices

    return result_values
