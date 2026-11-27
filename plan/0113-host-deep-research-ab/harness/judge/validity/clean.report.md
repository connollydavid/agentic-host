# The harness pin and the route behind it

The experiment pins one OpenCode release so no arm can win by running a different engine: `v2.4.2`, whose extracted binary hashes to `523b1502d1d556998b0904235cef65eb1d8cf8362b4e2faa7ae7a170c9a44cd4` [1]. The release tag, the archive digest and the binary digest are checked before every draw, and a wrong digest or version refuses the draw [1].

The reference model's stable identity is its deployment id. The router's `qwen3.8-flash-next` name resolves through the `qwen*` wildcard, so the deployment id `64e4a3742445b5bf58b5e6b75f83b9a84b87cfe19b47692b7984419f71804bf6` is the pin [2]. Pinning the deployment rather than the spelling is what makes a foreign model or a drifted route detectable: a reply that carries another model id is void [2].

Read together, the two pins answer different questions. The release pin fixes the harness the arm runs inside; the deployment pin fixes the model that answers. Either one drifting would make the A/B a comparison of two engines rather than two research approaches, which is why both are checked in pre-flight rather than recorded after the fact.
