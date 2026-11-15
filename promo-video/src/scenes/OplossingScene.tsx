import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {alpha, KlantConfig} from '../config';
import {Card, CardHeader, CheckIcon, Cursor, SceneShell, StepBadge, Subtitle, useSpring} from '../components/ui';

const RIJ_H = 136;
const RIJ_GAP = 22;

export const OplossingScene: React.FC<{config: KlantConfig; duration: number}> = ({config, duration}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const k = config.kleuren;
	const s = config.scenes.oplossing;
	const gekozen = s.gekozenIndex;

	const klik = 58;
	const vink = useSpring(klik, {damping: 11, stiffness: 220});
	const prijs = useSpring(klik + 22, {damping: 8, stiffness: 160, mass: 0.9});
	const prijsPuls = 1 + Math.max(0, Math.sin((frame - klik - 40) / 7)) * 0.03 * (frame > klik + 40 ? 1 : 0);

	// Cursor beweegt naar de gekozen optie
	const kaartTop = 400;
	const rijenTop = kaartTop + 48 + 90; // padding + header
	const doelY = rijenTop + gekozen * (RIJ_H + RIJ_GAP) + RIJ_H / 2 - 10;
	const cursorT = interpolate(frame, [26, klik - 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const ease = 1 - Math.pow(1 - cursorT, 3);
	const cx = interpolate(ease, [0, 1], [900, 190]);
	const cy = interpolate(ease, [0, 1], [1500, doelY]);
	const pressed = interpolate(frame, [klik - 3, klik, klik + 5], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const cursorOpacity = interpolate(frame, [20, 28, klik + 20, klik + 30], [0, 1, 1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<SceneShell duration={duration}>
			<StepBadge tekst={s.badge} kleuren={k} />
			<Card kleuren={k} top={kaartTop} delay={8}>
				<CardHeader titel={s.kaartTitel} kleuren={k} />
				<div style={{display: 'flex', flexDirection: 'column', gap: RIJ_GAP}}>
					{s.opties.map((optie, i) => {
						const isGekozen = i === gekozen;
						const rijIn = spring({frame: frame - 14 - i * 6, fps, config: {damping: 14, stiffness: 140, mass: 0.8}});
						const actief = isGekozen ? vink : 0;
						const dim = !isGekozen ? interpolate(vink, [0, 1], [1, 0.45]) : 1;
						return (
							<div
								key={optie}
								style={{
									height: RIJ_H,
									boxSizing: 'border-box',
									display: 'flex',
									alignItems: 'center',
									gap: 28,
									padding: '0 32px',
									borderRadius: 26,
									background: isGekozen ? alpha(k.accent, 0.08 + 0.14 * actief) : alpha(k.tekst, 0.03),
									border: `3px solid ${isGekozen && actief > 0.05 ? k.accent : k.kaartRand}`,
									boxShadow: isGekozen ? `0 0 ${50 * actief}px ${alpha(k.accent, 0.45)}` : 'none',
									opacity: rijIn * dim,
									transform: `translateX(${interpolate(rijIn, [0, 1], [80, 0])}px) scale(${1 + 0.03 * actief})`,
								}}
							>
								<div
									style={{
										width: 64,
										height: 64,
										borderRadius: 18,
										flexShrink: 0,
										border: `4px solid ${isGekozen && actief > 0.05 ? k.accent : k.tekstZacht}`,
										background: isGekozen ? alpha(k.accent, actief) : 'transparent',
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
									}}
								>
									{isGekozen ? <CheckIcon size={48} progress={actief} /> : null}
								</div>
								<div style={{fontSize: isGekozen ? 44 : 40, fontWeight: isGekozen ? 900 : 700, lineHeight: 1.15}}>{optie}</div>
							</div>
						);
					})}
				</div>
				<div style={{height: 300}} />
			</Card>

			{/* Gele prijsbadge */}
			<div
				style={{
					position: 'absolute',
					top: kaartTop + 48 + 90 + 3 * RIJ_H + 2 * RIJ_GAP + 50,
					left: 0,
					right: 0,
					display: 'flex',
					justifyContent: 'center',
				}}
			>
				<div
					style={{
						background: k.prijs,
						color: '#111827',
						borderRadius: 32,
						padding: '30px 56px',
						textAlign: 'center',
						transform: `scale(${interpolate(prijs, [0, 1], [0, 1]) * prijsPuls}) rotate(${interpolate(prijs, [0, 1], [-14, -3])}deg)`,
						boxShadow: `0 30px 70px ${alpha(k.prijs, 0.35)}, 0 0 0 8px ${alpha(k.prijs, 0.18)}`,
					}}
				>
					<div style={{fontSize: 84, fontWeight: 900, letterSpacing: -2, lineHeight: 1}}>{s.prijsRegel1}</div>
					<div style={{fontSize: 40, fontWeight: 800, marginTop: 12}}>{s.prijsRegel2}</div>
				</div>
			</div>

			<div style={{opacity: cursorOpacity}}>
				<Cursor x={cx} y={cy} pressed={pressed} />
			</div>
			<Subtitle tekst={s.ondertitel} kleuren={k} delay={16} />
		</SceneShell>
	);
};
