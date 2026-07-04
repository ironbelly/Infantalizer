# VENDOR.md — Adopted-file manifest

upstream_repo: https://github.com/haowjy/creative-writing-skills
upstream_sha:  3338495f0fabf778720effdda9386ab56d4ebf6e
vendored_on:   2026-07-03
license:       Apache-2.0 (upstream) — attribution retained per NOTICE
prefix_rewrite: "creative-writing-skills:" -> "laf-adaptation:"   # uniform, deterministic

## Invariants (asserted by check_boundary.py)
- G3 quartet-intact: agents/{critic,editor,reader-sim,continuity-checker}.md are ADOPTED-CLEAN and present.
- editor.md is NEVER folded, NEVER modified.
- No NATIVE/BUILD-NEW file name collides with an upstream file name.

<!-- Re-vendor / refresh: to re-vendor at a new upstream_sha, run
     `uv run python scripts/check_boundary.py --init --upstream <checkout>` then commit the manifest diff
     (see UPSTREAM-SYNC.md, authored in Phase 4). Do not hand-edit the manifest table below — it is
     machine-generated. -->

## Manifest

| path | class | upstream_sha256 | laf_sha256 |
|------|-------|-----------------|------------|
| agents/brainstormer.md | ADOPTED-CLEAN | aa736c5d23c3930576d449dbda56dfaf45d9c5f5273c466b9e1f36525117fa73 | 5c827effb5dc03364e339f3657356218dcb00288a596efc427e2c3e79a5752bc |
| agents/character-sim.md | ADOPTED-CLEAN | 0aa5a3459c5208e756f86e83ea99da70deac4c1e0f49b67018520b7287ad2494 | c7fcfc91a6d60bd4af3f555ce6e6c148f0a39887ff57ef136838b15c15ae75ed |
| agents/continuity-checker.md | ADOPTED-CLEAN | 0266f3368ef2549415c195f5379e8b185db9b2d9db4edaf0ee79e922a07ddf23 | 28a3c7eb7870ec29972da3da80c2baee093d621c5df4f3c3aa3ef56a364861cc |
| agents/critic.md | ADOPTED-CLEAN | a509d77fecd54b3fbd0ae771747ae63d6a65809cef739116c317ca70693bc62d | 9a0078e943c564010b8e1211e98b5a3b781ab9d7628f4ce06c39243d026ec21b |
| agents/editor.md | ADOPTED-CLEAN | afddbb5cad419421c93ff43d418ffceaeb54bd0f088abb3f2434e60253c9df09 | 2645f358fdc0f6b011479fa27195ba096c3836d2c6c4e7955bd78c1da82410e3 |
| agents/muse.md | ADOPTED-CLEAN | c8819ec80ee2734ac00257adf91ffd710b2916b99d9792946cfcc814c4b7b9a4 | 18cafdc251a528f0186d2d74135ae94cad0d05d37d2bf8f399a134969409af8f |
| agents/outliner.md | ADOPTED-CLEAN | fe78b2146e82f617d541e700051b803e9e8d9023993bc31f0e9df9de258de0c6 | d7b4b6e169c68da805178f4199129296afbeee52080abbb0ffb05059d13c2aaa |
| agents/reader-sim.md | ADOPTED-CLEAN | 06296b32dcf2932614ab032584334b3bcf3d1ab9c3802d0e09a47e9ac024b49b | 902a04a3aae0f784b3556c67c1a21bf4ffd69942d6a257bda06991ca58051bcf |
| agents/style-creator.md | ADOPTED-CLEAN | 24741d85da39edf08a489ab4a3061e3d38d3d9250dbf58dfab44f9e27c6295ba | 655ed29aba168a709bd7be95bbaa226d87bb9e0f72e3299d15d67a1d569251b4 |
| agents/web-researcher.md | ADOPTED-CLEAN | 0219d3d285b5a3b7b364860eebd956808bc9dbcb53d4ff4ea40ef2ebd41e4bb1 | fe3716801468128ec3f8408735c7b0bd03b333b76717e68097ba4420b9dc0ab3 |
| agents/writer.md | ADOPTED-PATCHED | 373e605b8e19dfa774af1036c61983f22cede1a5cb4748039ef48a142d769290 | c1b3e12f949db60f5e8a2d526ce917aef6328e845e2d20f031a57a9e52e09534 |
| skills/creative-research/SKILL.md | ADOPTED-CLEAN | ce1296b244700f98859d50be59c609e3a7523563eab773e9a96229c8052798f4 | ce1296b244700f98859d50be59c609e3a7523563eab773e9a96229c8052798f4 |
| skills/creative-writing-craft/SKILL.md | ADOPTED-CLEAN | 5c15d7f8f0d0ba2a75718f347a854b940f6262c4cd85c38531eb69039cd86c5d | 5c15d7f8f0d0ba2a75718f347a854b940f6262c4cd85c38531eb69039cd86c5d |
| skills/creative-writing-craft/resources/genre/fantasy.md | ADOPTED-CLEAN | b7cf6c8a25814f4bde30a6181337df5ea2c5596c5d0d35a8dd49409f83d18a64 | b7cf6c8a25814f4bde30a6181337df5ea2c5596c5d0d35a8dd49409f83d18a64 |
| skills/creative-writing-craft/resources/genre/horror.md | ADOPTED-CLEAN | f72591459e5cb53be93ebc092906b07d6f93aabb9b1a4ad806833bd683c1c38b | f72591459e5cb53be93ebc092906b07d6f93aabb9b1a4ad806833bd683c1c38b |
| skills/creative-writing-craft/resources/genre/litfic.md | ADOPTED-CLEAN | 181e3d51cceb5799acb48572ebfc7aa1a4e774c94894314fb12cb2c28557e00b | 181e3d51cceb5799acb48572ebfc7aa1a4e774c94894314fb12cb2c28557e00b |
| skills/creative-writing-craft/resources/genre/mystery.md | ADOPTED-CLEAN | b864c7380d2f12fcb8b0595041e024d0084943d1e8057d01b5bf18b24454b9aa | b864c7380d2f12fcb8b0595041e024d0084943d1e8057d01b5bf18b24454b9aa |
| skills/creative-writing-craft/resources/genre/romance.md | ADOPTED-CLEAN | 3384eaf17c13a0ddda80f152c0c65ad584068b9878fcc44f12dc4370ed581d38 | 3384eaf17c13a0ddda80f152c0c65ad584068b9878fcc44f12dc4370ed581d38 |
| skills/creative-writing-craft/resources/genre/thriller.md | ADOPTED-CLEAN | 25dbe3dfa00754e633d9a3f59e96d14db54bf4bcc532f2d2e8f3ad0e2d7cbb5c | 25dbe3dfa00754e633d9a3f59e96d14db54bf4bcc532f2d2e8f3ad0e2d7cbb5c |
| skills/creative-writing-craft/resources/prose-writing.md | ADOPTED-CLEAN | a78943d1fd9ab8fec738728f91ce81eeb007bf095ff6c8b3c40745899aa5a2d5 | a78943d1fd9ab8fec738728f91ce81eeb007bf095ff6c8b3c40745899aa5a2d5 |
| skills/creative-writing-craft/resources/scene-construction.md | ADOPTED-CLEAN | fce22dd09fb5df23bcbc09ea0a4429ab91915c5a9fc3fa9b4df5d0af77f0a3f8 | fce22dd09fb5df23bcbc09ea0a4429ab91915c5a9fc3fa9b4df5d0af77f0a3f8 |
| skills/creative-writing-craft/resources/style-analysis.md | ADOPTED-CLEAN | 2168822637fd4af215b3fdfe29d4958908828440aa6efff256092e9c91d28c28 | 2168822637fd4af215b3fdfe29d4958908828440aa6efff256092e9c91d28c28 |
| skills/creative-writing-modes/SKILL.md | ADOPTED-CLEAN | bb843dc5f4f5bbf4c2cc7e6bbeca4d8477873c2f8c87f6d4666567e4ddaa0ff6 | bb843dc5f4f5bbf4c2cc7e6bbeca4d8477873c2f8c87f6d4666567e4ddaa0ff6 |
| skills/creative-writing-modes/resources/prose-modes.md | ADOPTED-CLEAN | 7147c339fc78fbf460cfbc1a2b92a627249aebba4dfce3f5c3ec72e4ef6841ea | 7147c339fc78fbf460cfbc1a2b92a627249aebba4dfce3f5c3ec72e4ef6841ea |
| skills/grill-with-docs/SKILL.md | ADOPTED-CLEAN | 1d7b1487bc08d7bb2aed4a2e582953446f1b356dc5e26e37cefce29e57fe476a | 1d7b1487bc08d7bb2aed4a2e582953446f1b356dc5e26e37cefce29e57fe476a |
| skills/intent-modeling/SKILL.md | ADOPTED-CLEAN | 7dfcb6f076c0a932fa56c8f494a92401644893daf12634d597c471642a5eac51 | 7dfcb6f076c0a932fa56c8f494a92401644893daf12634d597c471642a5eac51 |
| skills/kb-management/SKILL.md | ADOPTED-CLEAN | 8953186d9bfa1e8599a0ef6364df7df35bf18ff6f82f753e5f3e18ffec4356c8 | 8953186d9bfa1e8599a0ef6364df7df35bf18ff6f82f753e5f3e18ffec4356c8 |
| skills/llm-writing/SKILL.md | ADOPTED-CLEAN | 16e502a27f4504e89affe9dd3eaca54c0082e3af1613734aac51e80aecf34037 | 16e502a27f4504e89affe9dd3eaca54c0082e3af1613734aac51e80aecf34037 |
| skills/shared-dao/SKILL.md | ADOPTED-CLEAN | 4422e8cfb22c93f43e54b67e7daf34cc427aac055216df0d8611aab109416600 | 4422e8cfb22c93f43e54b67e7daf34cc427aac055216df0d8611aab109416600 |
| skills/story-memory/SKILL.md | ADOPTED-CLEAN | fc74252a734f03d6152ca1be44577f384edc28d5b5bea260abd0c0a8661722fc | fc74252a734f03d6152ca1be44577f384edc28d5b5bea260abd0c0a8661722fc |
| skills/story-memory/resources/fact-extraction.md | ADOPTED-CLEAN | e48de1bd2191a5fd9dd85970685c1c727532475caf448f7dadd975c55117ccff | e48de1bd2191a5fd9dd85970685c1c727532475caf448f7dadd975c55117ccff |
| skills/story-memory/resources/story-context.md | ADOPTED-CLEAN | 6130c6924e258483700b7572fb1821d3f01e268386a7d4b6726839dc422e4fe6 | 6130c6924e258483700b7572fb1821d3f01e268386a7d4b6726839dc422e4fe6 |
| skills/story-memory/resources/story-reference-writing.md | ADOPTED-CLEAN | 71b903f6355f344d78d5a223d2a2841a63c197398cc8b2335c995ec298dacdc4 | 71b903f6355f344d78d5a223d2a2841a63c197398cc8b2335c995ec298dacdc4 |
| skills/story-memory/resources/story-reference-writing/reference-modes.md | ADOPTED-CLEAN | 62fd784f4f3cc5bf82cdeeed56d67fed64074e4f0c3caa2cd30ea1f323fa0b84 | 62fd784f4f3cc5bf82cdeeed56d67fed64074e4f0c3caa2cd30ea1f323fa0b84 |
| skills/story-memory/resources/writing-artifacts.md | ADOPTED-CLEAN | 995eeb5da2841a743db231ee5c9dec1b401a51a200eb825fef9bc3616b7a823b | 995eeb5da2841a743db231ee5c9dec1b401a51a200eb825fef9bc3616b7a823b |
| skills/story-memory/resources/writing-issues.md | ADOPTED-CLEAN | ffc0799bdc71711b68e88f9a6fb56d9af4a855037f6d87752b11b6c9683e08fc | ffc0799bdc71711b68e88f9a6fb56d9af4a855037f6d87752b11b6c9683e08fc |
| skills/story-review/SKILL.md | ADOPTED-CLEAN | f2a3996a2a6639ab9594056711130c031c11a01119856c2f0ab9e02bab2ae750 | f2a3996a2a6639ab9594056711130c031c11a01119856c2f0ab9e02bab2ae750 |
| skills/story-review/resources/copyedit.md | ADOPTED-CLEAN | 99600e56a1d6e9c7cac297f04b85e194318b9017c49c420fb158fcb3e7d4d640 | 99600e56a1d6e9c7cac297f04b85e194318b9017c49c420fb158fcb3e7d4d640 |
| skills/story-review/resources/developmental-edit.md | ADOPTED-CLEAN | b6317b7c8ef68943ab4ad10d3abfdc8ce5fbdbbfcfeb2ab3fe69c6733ed51667 | b6317b7c8ef68943ab4ad10d3abfdc8ce5fbdbbfcfeb2ab3fe69c6733ed51667 |
| skills/story-review/resources/editorial-review.md | ADOPTED-CLEAN | d731f237daa15d8df9513521bec5b7836d1f5393421018ca8d82a12511c66fbc | d731f237daa15d8df9513521bec5b7836d1f5393421018ca8d82a12511c66fbc |
| skills/story-review/resources/line-edit.md | ADOPTED-CLEAN | 9b98ee377b359a4858708a4ada2c361d3d3612bcf6486d2ee4e922f4d59e1020 | 9b98ee377b359a4858708a4ada2c361d3d3612bcf6486d2ee4e922f4d59e1020 |
| skills/story-review/resources/proofreading.md | ADOPTED-CLEAN | 9f59f9ce71c2722e23e10cf7b69d7073afbd6748aa6101ba9911cb4b1e000a04 | 9f59f9ce71c2722e23e10cf7b69d7073afbd6748aa6101ba9911cb4b1e000a04 |
| skills/story-review/resources/prose-critique.md | ADOPTED-CLEAN | cf5048f196a2f8a497d62574daf4ca8e6cf8ea138b916c08f265e4e0e141e2a7 | cf5048f196a2f8a497d62574daf4ca8e6cf8ea138b916c08f265e4e0e141e2a7 |
| skills/story-review/resources/prose-critique/analyze.py | ADOPTED-CLEAN | a57a66caed3efa3a3c0486580d64a573a64cf8caac7deb13ead8e64c4780da80 | a57a66caed3efa3a3c0486580d64a573a64cf8caac7deb13ead8e64c4780da80 |
| skills/story-review/resources/prose-critique/antipatterns.md | ADOPTED-CLEAN | b165830d65ba117929b9e337cb722bf993327086b4de6b3683866fe0fd42b547 | b165830d65ba117929b9e337cb722bf993327086b4de6b3683866fe0fd42b547 |
| skills/story-review/resources/prose-critique/baseline.md | ADOPTED-CLEAN | e6e48bd28c523ddbac6a280800aac7891dfdaeae3e81f8e3ec1a69d4f900bef2 | e6e48bd28c523ddbac6a280800aac7891dfdaeae3e81f8e3ec1a69d4f900bef2 |
| skills/story-review/resources/prose-critique/character.md | ADOPTED-CLEAN | 2836fe8ab432f5b9b48cbe603797bbcbb9c22c416ec23d743539fbcfbf4ae621 | 2836fe8ab432f5b9b48cbe603797bbcbb9c22c416ec23d743539fbcfbf4ae621 |
| skills/story-review/resources/prose-critique/continuity.md | ADOPTED-CLEAN | 6fd3b0fe94c6aeb7983afe79cb3131b58b9c59efdc3867cdf1201a10f9383d16 | 6fd3b0fe94c6aeb7983afe79cb3131b58b9c59efdc3867cdf1201a10f9383d16 |
| skills/story-review/resources/prose-critique/prose.md | ADOPTED-CLEAN | 71fccfaecdc64b1b74cb2ea448bf6bec8669a457306e29039f0445640da592cf | 71fccfaecdc64b1b74cb2ea448bf6bec8669a457306e29039f0445640da592cf |
| skills/story-review/resources/prose-critique/structure.md | ADOPTED-CLEAN | 785481adbbdf5672d93b0c0bf0774b8479476e496dc314b1244b3e4ee34bb490 | 785481adbbdf5672d93b0c0bf0774b8479476e496dc314b1244b3e4ee34bb490 |
| skills/story-review/resources/prose-critique/voice.md | ADOPTED-CLEAN | 23554d2011c13b942dae08b71177ffbac5d6a9d8c285d7e8ac35c8704cc8ae97 | 23554d2011c13b942dae08b71177ffbac5d6a9d8c285d7e8ac35c8704cc8ae97 |
| skills/story-review/resources/reader-sim-signal.md | ADOPTED-CLEAN | f25b4421ce0cb67e95a181aa0cc01aec27aac252a1502bb948ddf93ecf39568a | f25b4421ce0cb67e95a181aa0cc01aec27aac252a1502bb948ddf93ecf39568a |
| skills/writing-principles/SKILL.md | ADOPTED-CLEAN | 2ee021e7ad3638d46e3425c4366d5d4e0f8d2cbd34f0142392c0807f12b72141 | 2ee021e7ad3638d46e3425c4366d5d4e0f8d2cbd34f0142392c0807f12b72141 |
| skills/writing-principles/resources/citations.md | ADOPTED-CLEAN | 56dc0d42609604826b63b3380fc46d998e26bb6e8b853d90827f8f4c5b4855a2 | 56dc0d42609604826b63b3380fc46d998e26bb6e8b853d90827f8f4c5b4855a2 |
| skills/writing-principles/resources/failure-modes.md | ADOPTED-CLEAN | 82da42f04e6c06864f679dc29ad67d90c89eca42006c1c4941a6dfe951e084ea | 82da42f04e6c06864f679dc29ad67d90c89eca42006c1c4941a6dfe951e084ea |
| skills/writing-staffing/SKILL.md | ADOPTED-CLEAN | 11a294ccb376b9d81dc40e6c58fde91df37c210182c7c20ce34ea6b532c49f45 | 11a294ccb376b9d81dc40e6c58fde91df37c210182c7c20ce34ea6b532c49f45 |
| agents/analyst.md | NATIVE | — | — |
| agents/safety-verifier.md | NATIVE | — | — |
| skills/adaptation-rules/** | NATIVE | — | — |
| skills/adaptation-tiers/** | NATIVE | — | — |
| skills/source-fidelity/** | NATIVE | — | — |
| agents/chronicler.md | BUILD-NEW | — | — |
| agents/tier-coordinator.md | BUILD-NEW | — | — |
| skills/adaptation-safety/** | BUILD-NEW | — | — |
