import rawConfig from '../klant-config.json';

export type KlantConfig = typeof rawConfig;
export const defaultConfig: KlantConfig = rawConfig;

// Vaste video-specificaties: 1080x1920, 30 fps, exact 23 s (690 frames).
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const DURATION_IN_FRAMES = 690;

// Scènetiming in frames (moet gelijk blijven aan SCENES in scripts/genereer_voiceover.py).
export const SCENES = {
	hook: {from: 0, duration: 120}, // 0 - 4 s
	check: {from: 120, duration: 120}, // 4 - 8 s
	oplossing: {from: 240, duration: 180}, // 8 - 14 s
	contact: {from: 420, duration: 120}, // 14 - 18 s
	eind: {from: 540, duration: 150}, // 18 - 23 s
} as const;

export const FONT = "'Inter', 'Segoe UI', Helvetica, Arial, sans-serif";

/** Mengt twee hex-kleuren (t = 0..1). */
export const mixHex = (a: string, b: string, t: number): string => {
	const pa = parseInt(a.slice(1), 16);
	const pb = parseInt(b.slice(1), 16);
	const ch = (p: number, s: number) => (p >> s) & 255;
	const m = (s: number) => Math.round(ch(pa, s) + (ch(pb, s) - ch(pa, s)) * t);
	return `rgb(${m(16)}, ${m(8)}, ${m(0)})`;
};

/** Hex-kleur met alpha (0..1). */
export const alpha = (hex: string, a: number): string => {
	const p = parseInt(hex.slice(1), 16);
	return `rgba(${(p >> 16) & 255}, ${(p >> 8) & 255}, ${p & 255}, ${a})`;
};
