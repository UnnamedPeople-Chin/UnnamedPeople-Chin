import os
import subprocess
import tempfile
import urllib.request
import recolor_arcade_svg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACTION_BUNDLE_URL = "https://raw.githubusercontent.com/abozanona/pacman-contribution-graph/main/github-action/dist/index.js"


def get_github_token():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=5,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


def generate_extended_bomberman():
    req = urllib.request.Request(ACTION_BUNDLE_URL, headers={"User-Agent": "UnnamedPeople-Chin-Bomberman-Builder"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        js = resp.read().decode("utf-8")

    # 1. Score any bomb placement that blasts contribution cells positively even if an open corridor exists
    js = js.replace(
        "const l=e?e.cost-r.cost:10;if(l<=0)continue;",
        "const l=e?Math.max(e.cost-r.cost,6):10;",
    )
    # 2. Prioritize bombing contribution cells (Ne) before walking directly to opponent (Oe)
    js = js.replace(
        "this.movementStrategies=[new De,new Ue,new Ie,new Te,new Oe,new Ne]",
        "this.movementStrategies=[new De,new Ue,new Ie,new Te,new Ne,new Oe]",
    )
    # 3. Prevent early KO before frame 340 so both bombers clear the contribution board first
    js = js.replace(
        "killPlayersInBlast(t,e){const n=[];for(const o of t.players)o.alive&&e.some((t=>t.x===o.x&&t.y===o.y))&&(o.kill(),n.push(o.id));return n}",
        "killPlayersInBlast(t,e){if(t.frameCount<340)return[];const n=[];for(const o of t.players)o.alive&&e.some((t=>t.x===o.x&&t.y===o.y))&&(o.kill(),n.push(o.id));return n}",
    )
    js = js.replace(
        "killPlayersInActiveExplosions(){for(const t of this.store.players)if(t.alive)for(const e of this.store.activeExplosions)if(e.contains(t)){t.kill(),e.markPlayerHit(t.id);break}}",
        "killPlayersInActiveExplosions(){if(this.store.frameCount<340)return;for(const t of this.store.players)if(t.alive)for(const e of this.store.activeExplosions)if(e.contains(t)){t.kill(),e.markPlayerHit(t.id);break}}",
    )
    # 4. Extend max simulation length from 400 to 480 frames
    js = js.replace(
        "this.alivePlayerCount()>1&&this.store.frameCount<400",
        "this.alivePlayerCount()>1&&this.store.frameCount<480",
    )

    tmp_js = os.path.join(tempfile.gettempdir(), "run_extended_bomberman.js")
    with open(tmp_js, "w", encoding="utf-8") as f:
        f.write(js)

    env = os.environ.copy()
    env["INPUT_GITHUB_USER_NAME"] = os.environ.get("GITHUB_REPOSITORY_OWNER", "UnnamedPeople-Chin")
    env["INPUT_GITHUB_TOKEN"] = get_github_token()
    env["INPUT_GAMES"] = "bomberman"
    env["INPUT_HIDE_MONTH_LABELS"] = "false"

    try:
        res = subprocess.run(["node", tmp_js], capture_output=True, text=True, cwd=BASE_DIR, env=env, check=True)
        print(res.stdout.strip())
    finally:
        if os.path.exists(tmp_js):
            os.remove(tmp_js)


if __name__ == "__main__":
    generate_extended_bomberman()
    recolor_arcade_svg.main()
