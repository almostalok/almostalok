<!-- ============================================================
ALMOSTALOK // TERMINAL PROFILE v2
Assets live in ./assets (animated SVGs, safe for GitHub READMEs).
Colour theme: #0D1117 bg · #A855F7 purple · #22D3EE cyan · #4ADE80 green
============================================================= -->

<div align="center">

<img src="./assets/header.svg" width="100%" alt="Alok Kumar Singh — Developer / Product Builder" />

<br>

<a href="https://almostalok.tech"><img src="https://img.shields.io/badge/PORTFOLIO-almostalok.tech-7C3AED?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio" /></a>
<a href="https://almostalokblogs.tech"><img src="https://img.shields.io/badge/BLOG-almostalokblogs.tech-22D3EE?style=for-the-badge&logo=hashnode&logoColor=0D1117" alt="Blog" /></a>
<a href="https://almostalokresume.tech"><img src="https://img.shields.io/badge/RESUME-almostalokresume.tech-4ADE80?style=for-the-badge&logo=readme&logoColor=0D1117" alt="Resume" /></a>

<a href="https://linkedin.com/in/alokkumarsingh"><img src="https://img.shields.io/badge/LINKEDIN-alokkumarsingh-0A66C2?style=for-the-badge" alt="LinkedIn" /></a>
<a href="https://twitter.com/almostalok"><img src="https://img.shields.io/badge/X-@almostalok-000000?style=for-the-badge&logo=x&logoColor=white" alt="X / Twitter" /></a>
<a href="https://instagram.com/almostalok"><img src="https://img.shields.io/badge/INSTAGRAM-@almostalok-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>
<a href="https://youtube.com/c/almostalok"><img src="https://img.shields.io/badge/YOUTUBE-almostalok-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" /></a>

<br><br>

<img src="https://komarev.com/ghpvc/?username=almostalok&label=PROFILE%20VIEWS&color=7C3AED&style=flat-square" alt="Profile views" />
<img src="https://img.shields.io/github/followers/almostalok?label=FOLLOWERS&style=flat-square&color=22D3EE&labelColor=0D1117" alt="Followers" />
<img src="https://img.shields.io/badge/BUILDING-Hospate-4ADE80?style=flat-square&labelColor=0D1117" alt="Building Hospate" />

</div>

<br>

<div align="center">
<img src="./assets/terminal.svg" width="100%" alt="Animated terminal: whoami, cat about.json, ./ship.sh" />
</div>

<br>

<img src="./assets/sec_about.svg" width="100%" alt="neofetch" />

<table>
<tr>
<td width="42%" valign="top">

<img src="./assets/almostalok-ascii-profile.png" width="100%" alt="almostalok ASCII profile portrait" />

</td>
<td width="58%" valign="top">

```ts
// profile.ts
const alok = {
  name:       "Alok Kumar Singh",
  handle:     "@almostalok",
  role:       ["Developer", "Product Builder"],
  building:   "Hospate",
  location:   "India",
  focus:      "Useful products, real people",
  education:  "Learning. Always.",
  philosophy: "Ship > Perfection",
  hobbies:    ["Code", "Coffee", "Ideas", "Overthinking"],
  funFact:    "My quick fixes become full features.",
} as const;

export default alok;
```

```ini
[system_status]
Building   = Hospate            █████████░ 90%
Learning   = System Design      ███████░░░ 70%
Exploring  = Product + Growth   ██████░░░░ 60%
Open_To    = Exciting Problems  ████████░░ 80%
Caffeine   = Necessary          ██████████ 100%
```

</td>
</tr>
</table>

<br>

<img src="./assets/sec_status.svg" width="100%" alt="system_status --live" />

<div align="center">
<img src="./assets/status.svg" width="100%" alt="Live gauges: Hospate 90%, System Design 70%, Product and Growth 60%, Exciting Problems 80%, Caffeine 100%" />
</div>

<br>

<img src="./assets/sec_hospate.svg" width="100%" alt="cat hospate.md" />

> **HOSPATE** — cleaner workflows for real people.
> Not another dashboard built only to impress a screenshot. Real problems. Real users. Real impact.

<div align="center">
<img src="./assets/pipeline.svg" width="100%" alt="Hospate pipeline: idea to ship with feedback loop" />
</div>

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#1a0f38','primaryTextColor':'#E6EDF3','primaryBorderColor':'#A855F7','lineColor':'#22D3EE','secondaryColor':'#0D1117','tertiaryColor':'#0D1117','fontFamily':'monospace'}}}%%
flowchart LR
    A([💡 idea]) --> B{{product decision}}
    B --> C[architecture]
    C --> D[/code/]
    D --> E{bug?}
    E -- yes --> F[fix]
    F --> D
    E -- no --> G([🚀 ship])
    G -. feedback .-> A

    classDef ship fill:#14532d,stroke:#4ADE80,color:#fff
    classDef bug fill:#7f1d1d,stroke:#F87171,color:#fff
    class G ship
    class E,F bug
```

```bash
#!/usr/bin/env bash
# ship.sh — the entire Hospate philosophy in a few lines
set -euo pipefail

echo "> compiling ideas..."
echo "> deleting unnecessary complexity..."
npm run build && npm test || echo "> bug found. fixing. again."
echo "> shipping anyway."
```

<br>

<img src="./assets/sec_stack.svg" width="100%" alt="ls ~/stack" />

<div align="center">
<img src="./assets/stack.svg" width="100%" alt="Tech stack grouped by frontend, backend, data and devops, tools and mindset" />
<br><br>
<img src="https://skillicons.dev/icons?i=html,css,js,ts,react,nextjs,tailwind,nodejs,express,nestjs&perline=10" alt="Frontend and backend icons" />
<br>
<img src="https://skillicons.dev/icons?i=python,java,graphql,mongodb,postgres,mysql,redis,docker,aws&perline=9" alt="Languages, data and infra icons" />
<br>
<img src="https://skillicons.dev/icons?i=git,linux,figma,jest,electron,arduino,selenium&perline=7" alt="Tooling icons" />
</div>

<br>

<img src="./assets/sec_stats.svg" width="100%" alt="analyze" />

<table>
<tr>
<td width="50%">
<img src="https://github-readme-stats.vercel.app/api?username=almostalok&show_icons=true&theme=radical&hide_border=true&bg_color=0D1117&include_all_commits=true&cache_seconds=86400" width="100%" alt="GitHub statistics" />
</td>
<td width="50%">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=almostalok&layout=donut&theme=radical&hide_border=true&bg_color=0D1117&langs_count=8&cache_seconds=86400" width="100%" alt="Most used languages" />
</td>
</tr>
</table>

<div align="center">
<img src="https://streak-stats.demolab.com/?user=almostalok&theme=radical&hide_border=true&background=0D1117" width="75%" alt="GitHub contribution streak" />
<br><br>
<img src="https://github-profile-trophy.vercel.app/?username=almostalok&theme=radical&no-frame=true&no-bg=true&margin-w=8&row=1&column=6" width="95%" alt="GitHub trophies" />
</div>

> *"A green square cannot deploy an API. But it looks pretty cool."*

<br>

<img src="./assets/sec_activity.svg" width="100%" alt="graph --telemetry" />

<div align="center">
<img src="https://github-readme-activity-graph.vercel.app/graph?username=almostalok&theme=react-dark&bg_color=0D1117&color=A855F7&line=A855F7&point=ffffff&area=true&hide_border=true&custom_title=almostalok%20%2F%2F%20commit%20telemetry" width="100%" alt="Contribution activity over the last year" />
<br><br>
<img src="https://raw.githubusercontent.com/almostalok/almostalok/output/github-contribution-grid-snake-dark.svg" width="100%" alt="Contribution graph eaten by a snake" />
</div>

<br>

<img src="./assets/sec_connect.svg" width="100%" alt="socials" />

<table>
<tr>
<td width="50%" valign="top">

```ini
[links]
Portfolio  = almostalok.tech
Blog       = almostalokblogs.tech
Resume     = almostalokresume.tech
Twitter    = @almostalok
LinkedIn   = /in/alokkumarsingh
Instagram  = @almostalok
YouTube    = /c/almostalok
```

</td>
<td width="50%" valign="top">

```bash
#!/usr/bin/env bash
# hire.sh
PROBLEM="${1:-something exciting}"

echo "> reading: $PROBLEM"
echo "> coffee: 100%"
echo "> let's build something"
echo "  worth shipping."
```

</td>
</tr>
</table>

<details>
<summary><code>coding_profiles@dev:~$ ./links</code> &nbsp;— challenge me in public</summary>

<br>

<!-- Replace each URL with your real profile link -->

| Judge | Judge |
|:--|:--|
| [LeetCode](https://leetcode.com/u/almostalok) | [HackerRank](https://www.hackerrank.com/profile/almostalok) |
| [Codeforces](https://codeforces.com/profile/almostalok) | [AtCoder](https://atcoder.jp/users/almostalok) |
| [CodeChef](https://www.codechef.com/users/almostalok) | [GeeksforGeeks](https://auth.geeksforgeeks.org/user/almostalok) |
| [HackerEarth](https://www.hackerearth.com/@almostalok) | [Topcoder](https://www.topcoder.com/members/almostalok) |

</details>

<br>

<img src="./assets/sec_help.svg" width="100%" alt="help" />

```ini
[available_commands]
whoami    = Know more about me
projects  = See what I'm building
tech      = My tech stack
stats     = GitHub analytics
socials   = Find me online
hire      = Let's build together
clear     = Because clean terminals = happy mind

; $ sudo hire_me
; > permission granted. let's build something worth shipping.
```

<div align="center">

<a href="https://www.buymeacoffee.com/almostalok"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="45" alt="Buy me a coffee" /></a>
&nbsp;
<a href="https://ko-fi.com/almostalok"><img src="https://cdn.ko-fi.com/cdn/kofi3.png?v=3" height="45" alt="Support on Ko-fi" /></a>

<br><br>

```bash
almostalok@dev:~$ ./shutdown
> process still running.   > feature queue not empty.
> curiosity still active.  > sleep.service still missing.
# "Still a work in progress... but the commits are getting better."
```

<img src="./assets/footer.svg" width="100%" alt="almostalok // end of process" />

</div>
