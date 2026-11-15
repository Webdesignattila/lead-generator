import {interpolate, useCurrentFrame} from 'remotion';
import {alpha, KlantConfig} from '../config';
import {Card, CardHeader, SceneShell, StepBadge, Subtitle, useSpring, WarningIcon} from '../components/ui';

const Waarschuwing: React.FC<{tekst: string; delay: number; k: KlantConfig['kleuren']}> = ({tekst, delay, k}) => {
	const s = useSpring(delay, {damping: 12, stiffness: 170});
	return (
		<div
			style={{
				height: interpolate(s, [0, 1], [0, 132], {extrapolateRight: 'clamp'}),
				marginBottom: interpolate(s, [0, 1], [0, 22], {extrapolateRight: 'clamp'}),
				overflow: 'hidden',
			}}
		>
			<div
				style={{
					height: 132,
					boxSizing: 'border-box',
					display: 'flex',
					alignItems: 'center',
					gap: 26,
					padding: '0 30px',
					borderRadius: 24,
					background: alpha(k.fout, 0.1),
					border: `2px solid ${alpha(k.fout, 0.6)}`,
					transform: `rotateX(${interpolate(s, [0, 1], [-80, 0])}deg) translateX(${interpolate(s, [0, 1], [-60, 0])}px)`,
					transformOrigin: 'top',
					opacity: s,
				}}
			>
				<div
					style={{
						width: 76,
						height: 76,
						borderRadius: 20,
						background: alpha(k.fout, 0.18),
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						flexShrink: 0,
					}}
				>
					<WarningIcon size={46} color={k.fout} />
				</div>
				<div style={{fontSize: 44, fontWeight: 800}}>{tekst}</div>
				<div style={{marginLeft: 'auto', fontSize: 52, fontWeight: 900, color: k.fout}}>✕</div>
			</div>
		</div>
	);
};

export const CheckScene: React.FC<{config: KlantConfig; duration: number}> = ({config, duration}) => {
	const frame = useCurrentFrame();
	const k = config.kleuren;
	const s = config.scenes.check;
	const start = 22;
	const stap = 20;
	const gevonden = s.waarschuwingen.filter((_, i) => frame >= start + i * stap + 4).length;

	// Scan-lijn
	const scanY = interpolate(frame % 50, [0, 50], [0, 100]);
	const scanAan = frame < start + s.waarschuwingen.length * stap;

	return (
		<SceneShell duration={duration}>
			<StepBadge tekst={s.badge} kleuren={k} />
			<Card kleuren={k} top={400} delay={8}>
				<CardHeader
					titel={s.kaartTitel}
					kleuren={k}
					rechts={
						<div
							style={{
								fontSize: 30,
								fontWeight: 800,
								color: gevonden > 0 ? k.fout : k.tekstZacht,
								background: alpha(gevonden > 0 ? k.fout : k.tekstZacht, 0.14),
								padding: '10px 22px',
								borderRadius: 999,
							}}
						>
							{gevonden > 0 ? `${gevonden} problemen` : 'Scannen…'}
						</div>
					}
				/>
				<div style={{position: 'relative', minHeight: 200}}>
					{s.waarschuwingen.map((w, i) => (
						<Waarschuwing key={w} tekst={w} delay={start + i * stap} k={k} />
					))}
					{scanAan ? (
						<div
							style={{
								position: 'absolute',
								left: -48,
								right: -48,
								top: `${scanY}%`,
								height: 4,
								background: `linear-gradient(90deg, transparent, ${k.accent}, transparent)`,
								boxShadow: `0 0 24px ${k.accent}`,
								opacity: 0.8,
							}}
						/>
					) : null}
				</div>
			</Card>
			<Subtitle tekst={s.ondertitel} kleuren={k} delay={12} />
		</SceneShell>
	);
};
