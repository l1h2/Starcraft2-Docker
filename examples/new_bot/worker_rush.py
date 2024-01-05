from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer


class WorkerRushBot(BotAI):
    async def on_start(self) -> None:
        print("Game started")

    async def on_step(self, iteration: int) -> None:
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
                print(f"Worker {worker.tag} sent to enemy start location")
            print("Worker rush started!")

    async def on_unit_destroyed(self, unit_tag: int) -> None:
        print(f"Unit {unit_tag} destroyed")


run_game(
    maps.get("CyberForestLE"),
    [Bot(Race.Zerg, WorkerRushBot()), Computer(Race.Protoss, Difficulty.Medium)],
    realtime=False,
)
