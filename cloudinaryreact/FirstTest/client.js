import {ReactInstance} from 'react-360-web';
//import listReactFiles from 'list-react-files';
function init(bundle, parent, options = {}) {
  const r360 = new ReactInstance(bundle, parent, {
    fullScreen: true,
    ...options,
  });
//listReactFiles(__dirname).then(files => console.log(files))
  r360.renderToSurface(
    r360.createRoot('SlideshowSample', {
      photos: [
        {uri: './static_assets/1.jpg', title: 'First experience', format: '2D'},
        {uri: './static_assets/2.jpg', title: 'Second experience', format: '2D'},
        {uri: './static_assets/3.jpg', title: 'Third experience', format: '2D'},
	{uri: './static_assets/4.jpg', title: 'Fourth experience', format: '2D'}
        //{uri: './static_assets/360_world.jpg', title: '360 World', format: '2D'},
        // Add your own 180 / 360 photos to this array,
        // with an associated title and format
      ],
    }),
    r360.getDefaultSurface(),
  );
}
window.React360 = {init};
