import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {Background} from './components/Background';
import {FONT, KlantConfig, SCENES} from './config';
import {CheckScene} from './scenes/CheckScene';
import {ContactScene} from './scenes/ContactScene';
import {EindScene} from './scenes/EindScene';
import {HookScene} from './scenes/HookScene';
import {OplossingScene} from './scenes/OplossingScene';

export const PromoVideo: React.FC<{config: KlantConfig}> = ({config}) => {
	return (
		<AbsoluteFill style={{fontFamily: FONT, color: config.kleuren.tekst}}>
			<Background kleuren={config.kleuren} />

			<Sequence from={SCENES.hook.from} durationInFrames={SCENES.hook.duration} name="1 Hook">
				<HookScene config={config} duration={SCENES.hook.duration} />
			</Sequence>
			<Sequence from={SCENES.check.from} durationInFrames={SCENES.check.duration} name="2 Check">
				<CheckScene config={config} duration={SCENES.check.duration} />
			</Sequence>
			<Sequence from={SCENES.oplossing.from} durationInFrames={SCENES.oplossing.duration} name="3 Oplossing">
				<OplossingScene config={config} duration={SCENES.oplossing.duration} />
			</Sequence>
			<Sequence from={SCENES.contact.from} durationInFrames={SCENES.contact.duration} name="4 Contact">
				<ContactScene config={config} duration={SCENES.contact.duration} />
			</Sequence>
			<Sequence from={SCENES.eind.from} durationInFrames={SCENES.eind.duration} name="5 Eind">
				<EindScene config={config} duration={SCENES.eind.duration} />
			</Sequence>

			<Audio src={staticFile(config.voiceover.bestand)} volume={config.voiceover.volume} />
		</AbsoluteFill>
	);
};
