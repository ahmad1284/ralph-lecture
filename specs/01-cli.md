# Spec: CLI Entry Point

## Job to be Done
User provides a topic string. The tool runs end-to-end and produces a single video file. No intermediate files surfaced to the user.

## Interface

```
python main.py "Fourier Transform"
python main.py "Gradient Descent" --voice en-GB-SoniaNeural
python main.py "Bayes' Theorem" --random-voice
```

## Behaviour
- Default: `--random-voice` (randomly picks from curated voice list in tts spec)
- Creates `output/{slug}/` directory where slug is kebab-case of topic
- Runs all pipeline stages in sequence: script → animation → tts → subtitles → composition
- Logs each stage to stdout with timing
- Final output: `output/{slug}/final.mp4`
- On completion prints: `Done: output/{slug}/final.mp4`
- On any stage failure: prints error with stage name and exits non-zero

## Pipeline Order
1. Script generation (produces script.json)
2. Animation (produces scenes/*.mp4)
3. TTS (produces audio/*.mp3 + audio/*.json word boundaries)
4. Subtitle generation (produces subtitles.srt)
5. Composition (produces final.mp4)

## Dependencies
- All pipeline stages are separate modules: `pipeline/script.py`, `pipeline/animation.py`, `pipeline/tts.py`, `pipeline/subtitles.py`, `pipeline/composition.py`
- main.py orchestrates them, passing the output dir path between stages
- Each stage reads/writes from the same `output/{slug}/` directory
