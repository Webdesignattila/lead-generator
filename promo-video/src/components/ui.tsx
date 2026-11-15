import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {alpha, KlantConfig} from '../config';

type Kleuren = KlantConfig['kleuren'];

/** In- en uitfaden van een complete scène (met lichte zoom). */
export const SceneShell: React.FC<{duration: number; children: React.ReactNode}> = ({duration, children}) => {
	const frame = useCurrentFrame();
	const fadeIn = interpolate(frame, [0, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const fadeOut = interpolate(frame, [duration - 8, duration], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const scale = interpolate(frame, [0, 10, duration - 8, duration], [1.04, 1, 1, 0.97], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	return <AbsoluteFill style={{opacity: Math.min(fadeIn, fadeOut), transform: `scale(${scale})`}}>{children}</AbsoluteFill>;
};

/** Spring-helper met vertraging in frames. */
export const useSpring = (delay: number, config: {damping?: number; stiffness?: number; mass?: number} = {}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: frame - delay, fps, config: {damping: 14, stiffness: 140, mass: 0.8, ...config}});
};

/** Badge linksboven, bv. "#1 CHECK JE WEBSITE". */
export const StepBadge: React.FC<{tekst: string; kleuren: Kleuren}> = ({tekst, kleuren}) => {
	const s = useSpring(4);
	const [nummer, ...rest] = tekst.split(' ');
	const heeftNummer = nummer.startsWith('#');
	return (
		<div
			style={{
				position: 'absolute',
				top: 150,
				left: 70,
				display: 'flex',
				alignItems: 'center',
				gap: 18,
				padding: '18px 30px 18px 18px',
				borderRadius: 22,
				background: alpha(kleuren.kaart, 0.92),
				border: `2px solid ${alpha(kleuren.accent, 0.55)}`,
				boxShadow: `0 20px 50px rgba(0,0,0,0.45), 0 0 40px ${alpha(kleuren.accent, 0.25)}`,
				transform: `translateX(${interpolate(s, [0, 1], [-420, 0])}px)`,
				opacity: s,
			}}
		>
			{heeftNummer ? (
				<div
					style={{
						background: kleuren.accent,
						color: '#fff',
						fontWeight: 900,
						fontSize: 40,
						borderRadius: 14,
						padding: '6px 16px',
					}}
				>
					{nummer}
				</div>
			) : null}
			<div style={{fontWeight: 800, fontSize: 40, letterSpacing: 2}}>{heeftNummer ? rest.join(' ') : tekst}</div>
		</div>
	);
};

/** Strakke UI-kaart die met een spring inspringt. */
export const Card: React.FC<{
	kleuren: Kleuren;
	delay?: number;
	top: number;
	width?: number;
	children: React.ReactNode;
	style?: React.CSSProperties;
}> = ({kleuren, delay = 8, top, width = 900, children, style}) => {
	const s = useSpring(delay, {damping: 13});
	return (
		<div
			style={{
				position: 'absolute',
				top,
				left: (1080 - width) / 2,
				width,
				borderRadius: 36,
				padding: 48,
				background: `linear-gradient(160deg, ${alpha(kleuren.kaart, 0.98)} 0%, ${alpha(kleuren.achtergrond, 0.98)} 100%)`,
				border: `2px solid ${kleuren.kaartRand}`,
				boxShadow: `0 40px 90px rgba(0,0,0,0.55), inset 0 1px 0 ${alpha(kleuren.tekst, 0.06)}`,
				transform: `translateY(${interpolate(s, [0, 1], [140, 0])}px) scale(${interpolate(s, [0, 1], [0.86, 1])})`,
				opacity: interpolate(s, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'}),
				boxSizing: 'border-box',
				...style,
			}}
		>
			{children}
		</div>
	);
};

/** Kaartkop met venster-bolletjes en titel. */
export const CardHeader: React.FC<{titel: string; kleuren: Kleuren; rechts?: React.ReactNode}> = ({titel, kleuren, rechts}) => (
	<div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 36}}>
		<div style={{display: 'flex', alignItems: 'center', gap: 20}}>
			<div style={{display: 'flex', gap: 10}}>
				{['#FF5F57', '#FEBC2E', '#28C840'].map((c) => (
					<div key={c} style={{width: 18, height: 18, borderRadius: 9, background: c}} />
				))}
			</div>
			<div style={{fontSize: 36, fontWeight: 700, color: kleuren.tekstZacht}}>{titel}</div>
		</div>
		{rechts}
	</div>
);

/**
 * Grote gecentreerde ondertitel onderin. Woorden tussen *sterretjes* krijgen de accentkleur.
 * Woorden springen één voor één in beeld.
 */
export const Subtitle: React.FC<{tekst: string; kleuren: Kleuren; delay?: number}> = ({tekst, kleuren, delay = 10}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const woorden: {w: string; accent: boolean}[] = [];
	tekst.split(/(\*[^*]+\*)/g).forEach((deel) => {
		if (!deel) return;
		const accent = deel.startsWith('*') && deel.endsWith('*');
		deel
			.replace(/\*/g, '')
			.split(' ')
			.filter(Boolean)
			.forEach((w) => woorden.push({w, accent}));
	});

	return (
		<div
			style={{
				position: 'absolute',
				left: 70,
				right: 70,
				bottom: 230,
				display: 'flex',
				flexWrap: 'wrap',
				justifyContent: 'center',
				columnGap: 20,
				rowGap: 6,
				textAlign: 'center',
			}}
		>
			{woorden.map(({w, accent}, i) => {
				const s = spring({frame: frame - delay - i * 2, fps, config: {damping: 12, stiffness: 180, mass: 0.6}});
				return (
					<span
						key={i}
						style={{
							display: 'inline-block',
							fontSize: 74,
							lineHeight: 1.15,
							fontWeight: 900,
							letterSpacing: -1,
							color: accent ? kleuren.accent : kleuren.tekst,
							textShadow: accent
								? `0 0 30px ${alpha(kleuren.accent, 0.6)}, 0 6px 18px rgba(0,0,0,0.8)`
								: '0 6px 18px rgba(0,0,0,0.85)',
							opacity: interpolate(s, [0, 0.5], [0, 1], {extrapolateRight: 'clamp'}),
							transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px) scale(${interpolate(s, [0, 1], [0.7, 1])})`,
						}}
					>
						{w}
					</span>
				);
			})}
		</div>
	);
};

/* ---------- Iconen ---------- */

export const CheckIcon: React.FC<{size?: number; color?: string; progress?: number}> = ({size = 40, color = '#fff', progress = 1}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none">
		<path
			d="M5 12.5l4.5 4.5L19 7.5"
			stroke={color}
			strokeWidth={3.2}
			strokeLinecap="round"
			strokeLinejoin="round"
			strokeDasharray={24}
			strokeDashoffset={24 * (1 - progress)}
		/>
	</svg>
);

export const WarningIcon: React.FC<{size?: number; color: string}> = ({size = 44, color}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none">
		<path d="M12 3L2 20h20L12 3z" fill={color} />
		<path d="M12 10v4.5" stroke="#fff" strokeWidth={2.4} strokeLinecap="round" />
		<circle cx={12} cy={17.3} r={1.3} fill="#fff" />
	</svg>
);

export const ChatIcon: React.FC<{size?: number; color?: string}> = ({size = 48, color = '#fff'}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none">
		<path
			d="M12 3a9 9 0 00-7.8 13.5L3 21l4.6-1.2A9 9 0 1012 3z"
			stroke={color}
			strokeWidth={2}
			strokeLinejoin="round"
		/>
		<path
			d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.6-2-1-1 .8a4.5 4.5 0 01-2.2-2.2l.8-1-1-2L9.5 8"
			fill={color}
		/>
	</svg>
);

export const GlobeIcon: React.FC<{size?: number; color: string}> = ({size = 44, color}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2}>
		<circle cx={12} cy={12} r={9} />
		<path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z" />
	</svg>
);

export const EyeIcon: React.FC<{size?: number; color: string}> = ({size = 44, color}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2}>
		<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" />
		<circle cx={12} cy={12} r={3} />
	</svg>
);

export const ClockIcon: React.FC<{size?: number; color: string}> = ({size = 44, color}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2} strokeLinecap="round">
		<circle cx={12} cy={12} r={9} />
		<path d="M12 7v5l3.5 2" />
	</svg>
);

/** Geanimeerde muiscursor. */
export const Cursor: React.FC<{x: number; y: number; pressed: number}> = ({x, y, pressed}) => (
	<div
		style={{
			position: 'absolute',
			left: x,
			top: y,
			transform: `scale(${1 - pressed * 0.18})`,
			transformOrigin: 'top left',
			filter: 'drop-shadow(0 10px 18px rgba(0,0,0,0.6))',
		}}
	>
		<svg width={78} height={92} viewBox="0 0 26 30">
			<path d="M2 2l20 11.5-8.6 1.8 4.6 9.5-3.6 1.7-4.6-9.6L3.3 22.6z" fill="#fff" stroke="#0B1020" strokeWidth={1.6} strokeLinejoin="round" />
		</svg>
	</div>
);
