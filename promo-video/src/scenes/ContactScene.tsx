import {interpolate, useCurrentFrame} from 'remotion';
import {alpha, KlantConfig} from '../config';
import {Card, CardHeader, ChatIcon, CheckIcon, Cursor, SceneShell, StepBadge, Subtitle, useSpring} from '../components/ui';

export const ContactScene: React.FC<{config: KlantConfig; duration: number}> = ({config, duration}) => {
	const frame = useCurrentFrame();
	const k = config.kleuren;
	const s = config.scenes.contact;

	const kaartTop = 420;
	const klik = 50;

	// Pulserende knop + uitdijende ring
	const puls = frame < klik ? 1 + Math.sin(frame / 5) * 0.025 : 1;
	const ringT = (frame % 30) / 30;
	const pressed = interpolate(frame, [klik - 3, klik, klik + 6], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const ripple = interpolate(frame, [klik, klik + 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

	// Cursor
	const knopY = kaartTop + 48 + 90 + 210 + 75;
	const t = interpolate(frame, [14, klik - 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const e = 1 - Math.pow(1 - t, 3);
	const cx = interpolate(e, [0, 1], [960, 640]);
	const cy = interpolate(e, [0, 1], [1550, knopY - 10]);
	const cursorOpacity = interpolate(frame, [10, 18, klik + 22, klik + 32], [0, 1, 1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const bevestiging = useSpring(klik + 12, {damping: 10, stiffness: 190});

	return (
		<SceneShell duration={duration}>
			<StepBadge tekst={s.badge} kleuren={k} />
			<Card kleuren={k} top={kaartTop} delay={8}>
				<CardHeader titel={s.kaartTitel} kleuren={k} />

				{/* Voorbeeld-ontwerp skeleton */}
				<div style={{display: 'flex', gap: 22, height: 180, marginBottom: 30}}>
					<div style={{flex: 1.3, borderRadius: 22, background: `linear-gradient(135deg, ${alpha(k.accent, 0.5)}, ${alpha(k.accent, 0.1)})`}} />
					<div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 16, justifyContent: 'center'}}>
						{[0.95, 0.75, 0.55].map((w) => (
							<div key={w} style={{height: 22, width: `${w * 100}%`, borderRadius: 11, background: alpha(k.tekstZacht, 0.22)}} />
						))}
					</div>
				</div>

				{/* WhatsApp-knop */}
				<div style={{position: 'relative', height: 150}}>
					{frame < klik ? (
						<div
							style={{
								position: 'absolute',
								inset: 0,
								borderRadius: 30,
								border: `4px solid ${k.goed}`,
								transform: `scale(${1 + ringT * 0.12}, ${1 + ringT * 0.4})`,
								opacity: 1 - ringT,
							}}
						/>
					) : null}
					<div
						style={{
							position: 'absolute',
							inset: 0,
							borderRadius: 30,
							background: `linear-gradient(180deg, #2BD66A, ${k.goed})`,
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							gap: 22,
							padding: '0 30px',
							boxShadow: `0 20px 60px ${alpha(k.goed, 0.5)}`,
							transform: `scale(${puls * (1 - pressed * 0.06)})`,
							overflow: 'hidden',
						}}
					>
						<ChatIcon size={60} />
						<div style={{fontSize: 40, fontWeight: 900, color: '#fff', lineHeight: 1.1, textAlign: 'center'}}>{s.knopTekst}</div>
						{ripple > 0 && ripple < 1 ? (
							<div
								style={{
									position: 'absolute',
									left: 640 - 90 - 500 * ripple,
									top: 75 - 500 * ripple,
									width: 1000 * ripple,
									height: 1000 * ripple,
									borderRadius: '50%',
									background: 'rgba(255,255,255,0.35)',
									opacity: 1 - ripple,
								}}
							/>
						) : null}
					</div>
				</div>

				{/* Bevestiging */}
				<div
					style={{
						marginTop: 34,
						display: 'flex',
						alignItems: 'center',
						gap: 24,
						padding: '26px 30px',
						borderRadius: 24,
						background: alpha(k.goed, 0.1),
						border: `2px solid ${alpha(k.goed, 0.5)}`,
						opacity: bevestiging,
						transform: `translateY(${interpolate(bevestiging, [0, 1], [40, 0])}px) scale(${interpolate(bevestiging, [0, 1], [0.8, 1])})`,
					}}
				>
					<div
						style={{
							width: 72,
							height: 72,
							borderRadius: 36,
							background: k.goed,
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							boxShadow: `0 0 30px ${alpha(k.goed, 0.6)}`,
						}}
					>
						<CheckIcon size={48} progress={bevestiging} />
					</div>
					<div style={{fontSize: 46, fontWeight: 900}}>{s.bevestiging}</div>
				</div>
			</Card>

			<div style={{opacity: cursorOpacity}}>
				<Cursor x={cx} y={cy} pressed={pressed} />
			</div>
			<Subtitle tekst={s.ondertitel} kleuren={k} delay={10} />
		</SceneShell>
	);
};
