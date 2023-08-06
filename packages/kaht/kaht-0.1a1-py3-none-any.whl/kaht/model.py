from typing import Protocol, List, Any, Generator, Union, Iterable, Literal
from torch.utils.data.dataloader import DataLoader
from torch.optim.optimizer import Optimizer
import torch
from logging import Logger
from .base import Transferable, SaveDelegate

MODE = Literal['eval', 'train']
SAVED_SUFFIX = Literal['_best', '_latest']
TEST_CHOICES = Literal['best', 'latest']


class KahtDataModule(Protocol, Transferable):
    def train_dataloader(self, *args, **kwargs) -> Generator[Transferable]:
        raise NotImplementedError

    def test_dataloader(self) -> Iterable[Transferable]: ...

    def valid_dataloader(self) -> Iterable[Transferable]: ...


class KahtModule(Protocol, Transferable):
    mode: MODE

    save_delegate: SaveDelegate

    def will_train(self, *args, **kwargs): ...

    def on_train_one_step_start(self, logger: Logger): ...

    def train_one_step(self, task_batch) -> torch.Tensor:
        raise NotImplementedError

    def configure_optimizer(self) -> Union[Optimizer, List[Optimizer]]: ...

    def train_steps_end(self, outputs: List[Any]): ...

    def will_test(self, *args, **kwargs): ...

    def test_one_task(self, batch): ...

    def on_test_end(self, outpus: List[Any]): ...

    def will_valid(self, *args, **kwargs): ...

    def valid_one_task(self, batch) -> Any: ...

    def on_valid_end(self, outpus: List[Any]): ...

    def params_for_clip(self): ...

    def report_every(self, losses: Iterable): ...

    def save(self, suffix: SAVED_SUFFIX) -> str:
        """ Save and return saved result.
        :param suffix:
        :return:
        """
        raise NotImplementedError

    @property
    def training(self) -> bool:
        return self.mode == 'train'

    def switch(self, mode: MODE):
        raise NotImplementedError
