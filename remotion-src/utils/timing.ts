export const FPS = 30;

export function secondsToFrames(s: number): number {
  return Math.round(s * FPS);
}

export function framesToSeconds(f: number): number {
  return f / FPS;
}

export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * Math.max(0, Math.min(1, t));
}

export function windowProgress(frame: number, startFrame: number, durationFrames: number): number {
  if (frame < startFrame) return 0;
  if (frame >= startFrame + durationFrames) return 1;
  return (frame - startFrame) / durationFrames;
}
