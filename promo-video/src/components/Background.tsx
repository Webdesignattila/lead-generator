import {AbsoluteFill, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {alpha, KlantConfig} from '../config';

const PARTICLES = 46;

export const Background: React.FC<{kleuren: KlantConfig['kleuren']}> = ({kleuren}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const glowShift = Math.sin(frame / 90) * 60;

	return (
		<AbsoluteFill style={{backgroundColor: kleuren.achtergrond, overflow: 'hidden'}}>
			{/* Zachte blauwe gloed */}
			<AbsoluteFill
				style={{
					background: `radial-gradient(circle at ${50 + glowShift / 20}% ${30 + glowShift / 30}%, ${alpha(
						kleuren.achtergrondGlow,
						0.85,
					)} 0%, transparent 55%), radial-gradient(circle at 80% 95%, ${alpha(kleuren.accent, 0.18)} 0%, transparent 45%)`,
				}}
			/>
			{/* Subtiel raster */}
			<AbsoluteFill
				style={{
					backgroundImage: `linear-gradient(${alpha(kleuren.accent, 0.05)} 1px, transparent 1px), linear-gradient(90deg, ${alpha(
						kleuren.accent,
						0.05,
					)} 1px, transparent 1px)`,
					backgroundSize: '72px 72px',
					backgroundPosition: `0px ${-(frame * 0.4) % 72}px`,
					maskImage: 'radial-gradient(circle at 50% 40%, black 0%, transparent 75%)',
					WebkitMaskImage: 'radial-gradient(circle at 50% 40%, black 0%, transparent 75%)',
				}}
			/>
			{/* Bewegende deeltjes */}
			{new Array(PARTICLES).fill(0).map((_, i) => {
				const size = 2 + random(`s${i}`) * 5;
				const speed = 0.4 + random(`v${i}`) * 1.2;
				const x = random(`x${i}`) * width + Math.sin(frame / (40 + random(`w${i}`) * 40) + i) * 18;
				const travel = height + 40;
				const y = travel - ((random(`y${i}`) * travel + frame * speed) % travel) - 20;
				const twinkle = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(frame / 18 + i * 1.7));
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: x,
							top: y,
							width: size,
							height: size,
							borderRadius: '50%',
							background: i % 5 === 0 ? kleuren.tekst : kleuren.accent,
							opacity: twinkle * (size / 7),
							boxShadow: `0 0 ${size * 3}px ${alpha(kleuren.accent, 0.8)}`,
						}}
					/>
				);
			})}
			{/* Vignet */}
			<AbsoluteFill style={{background: 'radial-gradient(circle at 50% 45%, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
		</AbsoluteFill>
	);
};
