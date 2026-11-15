import '@fontsource/inter/500.css';
import '@fontsource/inter/700.css';
import '@fontsource/inter/800.css';
import '@fontsource/inter/900.css';
import {Composition} from 'remotion';
import {PromoVideo} from './PromoVideo';
import {defaultConfig, DURATION_IN_FRAMES, FPS, HEIGHT, WIDTH} from './config';

export const RemotionRoot: React.FC = () => {
	return (
		<Composition
			id="PromoVideo"
			component={PromoVideo}
			durationInFrames={DURATION_IN_FRAMES}
			fps={FPS}
			width={WIDTH}
			height={HEIGHT}
			defaultProps={{config: defaultConfig}}
		/>
	);
};
