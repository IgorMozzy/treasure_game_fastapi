from fastapi import FastAPI

from game import Game

# uvicorn api:app - ввести в терминале для запуска веб-сервера, ctrl+c в терминале для остановки
# uvicorn api:app --reload - автоматически перезагружает сервер после любых изменений в коде


app = FastAPI()


sessions = {}

@app.get("/game")
async def gg(name: str, coord='A 1'):
    if not sessions.get(name):
        game = Game()
        gamedict = {name: name,
                    'session': game
                    }
        sessions[name] = gamedict

        res = [f'Игра началась, {name}, следуйте шаблону A-1']

        for row in game.map.matrix:
            res.append(''.join(row))

        return [*res]
    else:
        player = sessions.get(name)
        game = player.get('session')

        r = game.start(coord)
        res = [r[0]]

        for row in game.map.matrix:
            res.append(''.join(row))

        if r[1] == 0:
            sessions.pop(name)

        return [*res]




