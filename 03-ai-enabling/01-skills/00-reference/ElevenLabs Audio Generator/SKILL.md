---
last_updated: 2026-02-25
status: active
name: elevenlabs-music
description: Generate music and sound effects using ElevenLabs API, then preview them in a web-based player. Use when asked to generate background music, sound effects, audio tracks, or songs for videos or projects. Triggers on "generate music", "make me some songs", "background music", "sound effects", "music for video", "audio tracks", "ElevenLabs music".
---

# ElevenLabs Audio Generator

Generate music, sound effects, and voice clips via ElevenLabs, preview in a grouped browser player.

## Define Done

- [ ] All requested audio tracks are generated and saved to the correct subdirectory (`music/`, `sfx/`, or `voice/`)
- [ ] Each audio file plays back clearly with no distortion, clipping, or truncation
- [ ] Voice clips match the requested text with natural cadence and correct pronunciation
- [ ] Music and sound effects match the requested mood, genre, and duration
- [ ] Duration falls within the valid range (0.5–30 seconds for music/sfx)
- [ ] All files are organized under the expected directory structure
- [ ] Browser player HTML is built and groups tracks by category with correct accent colors
- [ ] Player is served locally and exposed via Cloudflare tunnel
- [ ] Tunnel URL is sent to the user for preview

## Setup
- `ELEVENLABS_API_KEY` must be set in `.env`

## Audio Types

### Music
```bash
bash scripts/generate.sh <output_dir>/music "<prompt>" [duration_seconds] [prompt_influence]
```
- `duration_seconds`: 0.5 to 30 (optional, API guesses if omitted)
- `prompt_influence`: 0 to 1, default 0.3 (higher = closer to prompt)
- Be specific: genre, mood, tempo, instruments, "no vocals"

### Sound Effects
```bash
bash scripts/generate.sh <output_dir>/sfx "<prompt>" [duration_seconds] [prompt_influence]
```
- Same API as music, just describe sounds instead of music
- Good for: whooshes, clicks, ambient, UI sounds, impacts

### Voice
```bash
bash scripts/generate_voice.sh <output_dir>/voice "<text>" [voice_id] [model_id]
```
- Default voice: Sarah (EXAVITQu4vr4xnSDxMaL)
- Default model: eleven_flash_v2_5
- Common voices: Roger (CwhRBWXzGAHq8TQ4Fs17), Charlie (IKne3meq5aSn9XLyUdCD), George (JBFqnCBsd6RMkjVDRZzb), River (SAz9YHcvj6GT2YYXdXww)

## Player

Build the grouped player (music/sfx/voice sections with different accent colors):
```bash
bash scripts/player.sh <base_dir> <output_html>
```

Expected directory structure:
```
<base_dir>/
├── music/*.mp3   (green accent)
├── sfx/*.mp3     (yellow accent)
└── voice/*.mp3   (blue accent)
```

Any category dir that exists gets included. Missing dirs are skipped.

## Quality Tests

| Test | PASS | FAIL |
|------|------|------|
| Audio playback | File plays without errors in browser player | File is silent, corrupted, or fails to load |
| Voice accuracy | Spoken text matches the requested script exactly | Words are mispronounced, skipped, or garbled |
| Music mood | Genre, tempo, and instruments match the prompt | Output sounds unrelated to the prompt |
| Duration | Track length is within the requested range | Track is too short, too long, or cut off abruptly |
| File format | Output is a valid `.mp3` file | File is empty, wrong format, or missing extension |
| Directory structure | Files land in the correct `music/`, `sfx/`, or `voice/` subdirectory | Files are in the wrong directory or at the base level |
| Player build | HTML player renders all categories with correct accent colors | Player is missing categories, broken, or shows no audio |
| Tunnel exposure | Public URL is reachable and streams audio | URL returns an error or audio fails to load remotely |

## Workflow

1. Generate tracks in parallel (one call per track, run with `&` and `wait`)
2. Organize into `music/`, `sfx/`, `voice/` subdirs
3. Build the player: `bash scripts/player.sh <base_dir> <output_html>`
4. Serve: `cd <base_dir> && nohup python3 -m http.server <port> > /dev/null 2>&1 &`
5. Expose: `bash skills/cloudflare-tunnel/scripts/tunnel.sh start <port>`
6. Send tunnel URL. User previews, selects favorites, asks for more.