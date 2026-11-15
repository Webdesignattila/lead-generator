import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {alpha, KlantConfig} from '../config';
import {Card, ClockIcon, EyeIcon, GlobeIcon, Subtitle, useSpring} from '../components/ui';

export const EindScene: React.FC<{config: KlantConfig; duration: number}> = ({config}) => {
	// Geen uitfade: het eindbeeld blijft tot het laatste frame staan.
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const k = config.kleuren;
	const m = config.merk;
	const l = config.scenes.eind;

	const fadeIn = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
	const logo = useSpring(4, {damping: 10, stiffness: 150});
	const naam = useSpring(14);
	const lijn = useSpring(22, {damping: 20});
	const glow = 0.5 + 0.5 * Math.sin(frame / 10);

	const rijen = [
		{icoon: <GlobeIcon color={k.accent} />, label: l.labelWebsite, waarde: m.website, groot: true},
		{icoon: <EyeIcon color={k.accent} />, label: l.labelBelofte, waarde: m.belofte, groot: false},
		{icoon: <ClockIcon color={k.accent} />, label: l.labelBereikbaar, waarde: m.bereikbaarheid, groot: false},
	];

	return (
		<div style={{position: 'absolute', inset: 0, opacity: fadeIn}}>
			{/* Logo */}
			<div style={{position: 'absolute', top: 170, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
				<div
					style={{
						width: 220,
						height: 220,
						borderRadius: 60,
						background: `linear-gradient(140deg, ${k.accent}, ${k.achtergrondGlow})`,
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						fontSize: 104,
						fontWeight: 900,
						letterSpacing: -4,
						boxShadow: `0 0 ${60 + glow * 50}px ${alpha(k.accent, 0.55)}, inset 0 2px 0 rgba(255,255,255,0.25)`,
						transform: `scale(${logo}) rotate(${interpolate(logo, [0, 1], [-25, 0])}deg)`,
					}}
				>
					{m.logoTekst}
				</div>
				<div
					style={{
						marginTop: 50,
						fontSize: 100,
						fontWeight: 900,
						letterSpacing: -3,
						opacity: naam,
						transform: `translateY(${interpolate(naam, [0, 1], [50, 0])}px)`,
						textShadow: '0 8px 24px rgba(0,0,0,0.7)',
					}}
				>
					{m.naam}
				</div>
				<div style={{marginTop: 22, height: 8, width: 360 * lijn, borderRadius: 4, background: k.accent, boxShadow: `0 0 24px ${k.accent}`}} />
			</div>

			{/* Contactkaart */}
			<Card kleuren={k} top={740} delay={26}>
				<div style={{display: 'flex', flexDirection: 'column', gap: 26}}>
					{rijen.map((r, i) => {
						const s = spring({frame: frame - 36 - i * 10, fps, config: {damping: 14, stiffness: 140, mass: 0.8}});
						return (
							<div
								key={r.label}
								style={{
									display: 'flex',
									alignItems: 'center',
									gap: 30,
									padding: '28px 30px',
									borderRadius: 26,
									background: r.groot ? alpha(k.accent, 0.14) : alpha(k.tekst, 0.03),
									border: `2px solid ${r.groot ? k.accent : k.kaartRand}`,
									opacity: s,
									transform: `translateX(${interpolate(s, [0, 1], [-70, 0])}px)`,
								}}
							>
								<div
									style={{
										width: 88,
										height: 88,
										borderRadius: 24,
										background: alpha(k.accent, 0.15),
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
										flexShrink: 0,
									}}
								>
									{r.icoon}
								</div>
								<div>
									<div style={{fontSize: 28, color: k.tekstZacht, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 2}}>{r.label}</div>
									<div style={{fontSize: r.groot ? 56 : 44, fontWeight: 900, color: r.groot ? k.accent : k.tekst, marginTop: 4}}>{r.waarde}</div>
								</div>
							</div>
						);
					})}
				</div>
			</Card>

			<Subtitle tekst={l.ondertitel} kleuren={k} delay={60} />
		</div>
	);
};
