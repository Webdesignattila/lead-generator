import {Easing, interpolate, useCurrentFrame} from 'remotion';
import {alpha, KlantConfig, mixHex} from '../config';
import {Card, CardHeader, SceneShell, Subtitle, useSpring, WarningIcon} from '../components/ui';

const GoogleG: React.FC = () => (
	<div
		style={{
			width: 56,
			height: 56,
			borderRadius: 28,
			background: '#fff',
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
			fontSize: 38,
			fontWeight: 900,
			color: '#4285F4',
		}}
	>
		G
	</div>
);

export const HookScene: React.FC<{config: KlantConfig; duration: number}> = ({config, duration}) => {
	const frame = useCurrentFrame();
	const k = config.kleuren;
	const s = config.scenes.hook;

	// Score zakt van groen naar rood
	const drop = interpolate(frame, [32, 82], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.bezier(0.65, 0, 0.35, 1),
	});
	const score = Math.round(interpolate(drop, [0, 1], [s.scoreStart, s.scoreEind]));
	const kleur = drop < 0.5 ? mixHex(k.goed, '#F59E0B', drop * 2) : mixHex('#F59E0B', k.fout, (drop - 0.5) * 2);

	const R = 170;
	const omtrek = 2 * Math.PI * R;
	const gaugeIn = useSpring(14, {damping: 20});
	const vulling = (score / 100) * gaugeIn;

	const label = useSpring(80, {damping: 9, stiffness: 200});
	const shake = frame > 80 && frame < 96 ? Math.sin(frame * 2.4) * (96 - frame) * 0.9 : 0;

	const metrics = [
		{naam: 'Laadtijd mobiel', goed: 0.9, slecht: 0.22},
		{naam: 'Vindbaarheid', goed: 0.86, slecht: 0.3},
		{naam: 'Gebruiksgemak', goed: 0.94, slecht: 0.35},
	];

	return (
		<SceneShell duration={duration}>
			<Card kleuren={k} top={250} delay={2}>
				<CardHeader
					titel={s.kaartTitel}
					kleuren={k}
					rechts={<GoogleG />}
				/>
				<div
					style={{
						fontSize: 32,
						color: k.tekstZacht,
						background: alpha(k.achtergrond, 0.8),
						border: `2px solid ${k.kaartRand}`,
						borderRadius: 18,
						padding: '16px 24px',
						marginBottom: 30,
					}}
				>
					🔒 {s.domein}
				</div>

				<div style={{position: 'relative', width: 420, height: 420, margin: '0 auto'}}>
					<svg width={420} height={420} style={{transform: 'rotate(-90deg)'}}>
						<circle cx={210} cy={210} r={R} stroke={alpha(k.tekstZacht, 0.15)} strokeWidth={30} fill="none" />
						<circle
							cx={210}
							cy={210}
							r={R}
							stroke={kleur}
							strokeWidth={30}
							fill="none"
							strokeLinecap="round"
							strokeDasharray={omtrek}
							strokeDashoffset={omtrek * (1 - vulling)}
							style={{filter: `drop-shadow(0 0 18px ${kleur})`}}
						/>
					</svg>
					<div
						style={{
							position: 'absolute',
							inset: 0,
							display: 'flex',
							flexDirection: 'column',
							alignItems: 'center',
							justifyContent: 'center',
						}}
					>
						<div style={{fontSize: 150, fontWeight: 900, color: kleur, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>
							{score}
							<span style={{fontSize: 70}}>%</span>
						</div>
						<div style={{fontSize: 30, color: k.tekstZacht, marginTop: 10, fontWeight: 700}}>Prestatiescore</div>
					</div>
				</div>

				<div style={{height: 100, display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 16}}>
					<div
						style={{
							display: 'flex',
							alignItems: 'center',
							gap: 16,
							padding: '16px 34px',
							borderRadius: 999,
							background: alpha(k.fout, 0.16),
							border: `3px solid ${k.fout}`,
							color: k.fout,
							fontSize: 42,
							fontWeight: 900,
							opacity: label,
							transform: `scale(${interpolate(label, [0, 1], [0.4, 1])}) translateX(${shake}px)`,
							boxShadow: `0 0 40px ${alpha(k.fout, 0.45)}`,
						}}
					>
						<WarningIcon size={46} color={k.fout} />
						{s.statusLabel}
					</div>
				</div>

				<div style={{marginTop: 20, display: 'flex', flexDirection: 'column', gap: 22}}>
					{metrics.map((m, i) => {
						const w = interpolate(drop, [0, 1], [m.goed, m.slecht]) * gaugeIn;
						const c = drop < 0.5 ? mixHex(k.goed, '#F59E0B', drop * 2) : mixHex('#F59E0B', k.fout, (drop - 0.5) * 2);
						return (
							<div key={i}>
								<div style={{fontSize: 28, color: k.tekstZacht, marginBottom: 8, fontWeight: 500}}>{m.naam}</div>
								<div style={{height: 16, borderRadius: 8, background: alpha(k.tekstZacht, 0.12)}}>
									<div style={{height: 16, width: `${w * 100}%`, borderRadius: 8, background: c}} />
								</div>
							</div>
						);
					})}
				</div>
			</Card>
			<Subtitle tekst={s.ondertitel} kleuren={k} delay={8} />
		</SceneShell>
	);
};
