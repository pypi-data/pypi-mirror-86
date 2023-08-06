/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a4/api/adapters/cqhttp.html",
    "revision": "da937f12466ead57bc9f39dbae8a15b8"
  },
  {
    "url": "2.0.0a4/api/adapters/index.html",
    "revision": "f71dc20a9a1b0274f1ac401458bb724e"
  },
  {
    "url": "2.0.0a4/api/config.html",
    "revision": "9bd56ea8b1090c4ecba687c16f156d27"
  },
  {
    "url": "2.0.0a4/api/drivers/fastapi.html",
    "revision": "8fa58df79e5d01d6156609e3a69df403"
  },
  {
    "url": "2.0.0a4/api/drivers/index.html",
    "revision": "a331fac66a80c5133dff25cc2169a542"
  },
  {
    "url": "2.0.0a4/api/exception.html",
    "revision": "2a75e6a4b53f074d2dea085733f875c9"
  },
  {
    "url": "2.0.0a4/api/index.html",
    "revision": "69600027071ac3eece449e1b191b8017"
  },
  {
    "url": "2.0.0a4/api/log.html",
    "revision": "54223e3b7657b9981758ec427cac041e"
  },
  {
    "url": "2.0.0a4/api/matcher.html",
    "revision": "9cef4d97eb2745d9b57dd9cf2c11500a"
  },
  {
    "url": "2.0.0a4/api/nonebot.html",
    "revision": "37a5c2fae7cb65e30caf23b05afcfc06"
  },
  {
    "url": "2.0.0a4/api/permission.html",
    "revision": "9ac56f418e46fdc0c8381f50719f09b5"
  },
  {
    "url": "2.0.0a4/api/plugin.html",
    "revision": "7a088340aa4fea38098b82cc4b3826d3"
  },
  {
    "url": "2.0.0a4/api/rule.html",
    "revision": "3fc754f23616a931115c3db1698f38ee"
  },
  {
    "url": "2.0.0a4/api/sched.html",
    "revision": "9fc25b07fff656035afa2def7fa406a1"
  },
  {
    "url": "2.0.0a4/api/typing.html",
    "revision": "d2868f18ca83acf85d3bea158650aa93"
  },
  {
    "url": "2.0.0a4/api/utils.html",
    "revision": "c31486b7c326c97a96d8b390f31bd11d"
  },
  {
    "url": "2.0.0a4/guide/basic-configuration.html",
    "revision": "c4e0ba4858b0d9a88590e844161e660e"
  },
  {
    "url": "2.0.0a4/guide/creating-a-project.html",
    "revision": "c29b3db461a7bf15446525c8e84714f2"
  },
  {
    "url": "2.0.0a4/guide/getting-started.html",
    "revision": "a577e84caad3d4c63dfb07b7a5e4db0b"
  },
  {
    "url": "2.0.0a4/guide/index.html",
    "revision": "ddb1c6929c3f0f982d7920d2e4e4754b"
  },
  {
    "url": "2.0.0a4/guide/installation.html",
    "revision": "4349e13c0735f9541f908455d84b344c"
  },
  {
    "url": "2.0.0a4/guide/writing-a-plugin.html",
    "revision": "ca928b001c159e9b936103dd3f69ad2a"
  },
  {
    "url": "2.0.0a4/index.html",
    "revision": "538514ae653be2d17dd6e64038463c4a"
  },
  {
    "url": "404.html",
    "revision": "247937ed18f01651baca1021c1b42dcd"
  },
  {
    "url": "advanced/index.html",
    "revision": "4f94a082d00604f7c51cbcd09c0ab9fb"
  },
  {
    "url": "advanced/permission.html",
    "revision": "0fd04c225acde22acfd4b5e0b58689d4"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "be0191b9d38096740ae9271c612215be"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "0e48d60653dd862e56f4c42b9ecb1607"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "471c4708f5697370f516d22c0ac7f1aa"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "b3d1a05b1cfead86df6e36f10e658812"
  },
  {
    "url": "api/config.html",
    "revision": "26e1cb687ac42c82d572cbacca2196f4"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "6a4817107407df4df1563a0beb4a3f38"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "62d549958d373f33e9754985dfb96814"
  },
  {
    "url": "api/exception.html",
    "revision": "cd7b2798de8221b60ad5e7ac9966cfd2"
  },
  {
    "url": "api/index.html",
    "revision": "56af9cbebd35b5ffb66de07e1e1b4d5e"
  },
  {
    "url": "api/log.html",
    "revision": "b7359484b5cbc77866ad5b8e4bfdf772"
  },
  {
    "url": "api/matcher.html",
    "revision": "437ffecd48c37db0cc4fee9e0965fe35"
  },
  {
    "url": "api/message.html",
    "revision": "06f1b95129c8d9145b96d45849710adb"
  },
  {
    "url": "api/nonebot.html",
    "revision": "1bd493a64dab28480296cc46d61f9761"
  },
  {
    "url": "api/permission.html",
    "revision": "229ac716f8abc1908dde1794a518080d"
  },
  {
    "url": "api/plugin.html",
    "revision": "8c272cc1044421312a3f7f36edce3ec8"
  },
  {
    "url": "api/rule.html",
    "revision": "bb9fa8ede14d599326a5728a662b0b61"
  },
  {
    "url": "api/sched.html",
    "revision": "f3be4b0b016585c443ddf4f49cea0aed"
  },
  {
    "url": "api/typing.html",
    "revision": "e5c47e17be076664458083cc8687467c"
  },
  {
    "url": "api/utils.html",
    "revision": "f44c78d1b123d75e8896c39d40a4bfaf"
  },
  {
    "url": "assets/css/0.styles.01d02d32.css",
    "revision": "3f027aabc0f5cdc758eebc8339818004"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.41f89dd3.js",
    "revision": "aa1a4b071deb6c6578b62132e97643bd"
  },
  {
    "url": "assets/js/11.4af81069.js",
    "revision": "882b9cadfe9b8e9a657cb0877bcf1ded"
  },
  {
    "url": "assets/js/12.068d7e5e.js",
    "revision": "ad5dbbf10c9e469e4b82027f54077687"
  },
  {
    "url": "assets/js/13.3f32848d.js",
    "revision": "24b96a5215f86c3eebee00c4da1d6efa"
  },
  {
    "url": "assets/js/14.17f9aa12.js",
    "revision": "66f044e8bc7193c80af3a1b56f62d6a4"
  },
  {
    "url": "assets/js/15.ca0effe8.js",
    "revision": "9e75648cdeab9d8e81d594e0e1a64540"
  },
  {
    "url": "assets/js/16.f2a78eaa.js",
    "revision": "e50365c90cd16eaade36b275bc759541"
  },
  {
    "url": "assets/js/17.6e4b53cc.js",
    "revision": "9701cbe2f25fa98400b892d781be4239"
  },
  {
    "url": "assets/js/18.409993d2.js",
    "revision": "9257c563ce35931b31d82224f22a87c4"
  },
  {
    "url": "assets/js/19.c2cff776.js",
    "revision": "31ac740d0ee59d6a99f98dff0addcd8c"
  },
  {
    "url": "assets/js/2.1a59183a.js",
    "revision": "5d8dafac5565d5e412fd956247219111"
  },
  {
    "url": "assets/js/20.14a69764.js",
    "revision": "38c95baaab60bf1d24c201cae4ca0738"
  },
  {
    "url": "assets/js/21.7061203c.js",
    "revision": "c3f5181a88e7098abad637bca62bfb1a"
  },
  {
    "url": "assets/js/22.8c456c61.js",
    "revision": "5b1ae7ea8682ab55fa5c12e6b145b85d"
  },
  {
    "url": "assets/js/23.c1f032a3.js",
    "revision": "29480cd98c4e82bad93b0e49334fe0f4"
  },
  {
    "url": "assets/js/24.1bec3016.js",
    "revision": "088faa11ad01c2146cdbb90da101e5e4"
  },
  {
    "url": "assets/js/25.f676453e.js",
    "revision": "842a8169f60fced23540ca934e827b46"
  },
  {
    "url": "assets/js/26.0d5cbaa1.js",
    "revision": "91af64c36b14045f5637f164e194db95"
  },
  {
    "url": "assets/js/27.0620b9b1.js",
    "revision": "84fa5def054d4ab78dafc6844e7cd914"
  },
  {
    "url": "assets/js/28.610ae5ee.js",
    "revision": "e8c2dc948ef5f5f72bb09c17f0f98c6a"
  },
  {
    "url": "assets/js/29.689f1425.js",
    "revision": "89a3de70c0c066416bc65b30b393fb7f"
  },
  {
    "url": "assets/js/3.4bfdb268.js",
    "revision": "117b26248350caf0435164fb2ee00b08"
  },
  {
    "url": "assets/js/30.77a52afe.js",
    "revision": "311837c3b016c8537cd31c7f93193fcc"
  },
  {
    "url": "assets/js/31.e9f9bc40.js",
    "revision": "8a331e8af8a43ebb1a1c4ada35ca5db7"
  },
  {
    "url": "assets/js/32.47065d2b.js",
    "revision": "db99b31f010ec674cc25dd4635336b36"
  },
  {
    "url": "assets/js/33.882c69d0.js",
    "revision": "0174d4f4373d986d96a34580deee649d"
  },
  {
    "url": "assets/js/34.24af286b.js",
    "revision": "d1dafb2ba8d4ef4894f7db01b32351dd"
  },
  {
    "url": "assets/js/35.d88de6dc.js",
    "revision": "971c753db3181ff36dc504dbbcc97710"
  },
  {
    "url": "assets/js/36.db71f5a0.js",
    "revision": "48c7180f0fbd04708f1f3dbd52712a3e"
  },
  {
    "url": "assets/js/37.081b20f9.js",
    "revision": "73e74fcc0bcda7838d55ff4f85108f5b"
  },
  {
    "url": "assets/js/38.ed19eca3.js",
    "revision": "34083a64cffb059f62a70d8686b12f85"
  },
  {
    "url": "assets/js/39.018ac36a.js",
    "revision": "6d82649ac14602e9edbaa05e43822c34"
  },
  {
    "url": "assets/js/4.fefb5760.js",
    "revision": "f9c6601b542c55dd38c610ffd6f585a2"
  },
  {
    "url": "assets/js/40.9590171c.js",
    "revision": "386de92169bdcd6c6850fa61585ccc20"
  },
  {
    "url": "assets/js/41.b67a2923.js",
    "revision": "5e02d626f94bcaa04f2c365d2d687d78"
  },
  {
    "url": "assets/js/42.0564389c.js",
    "revision": "d96946170aabbcc62c011552641e51d6"
  },
  {
    "url": "assets/js/43.a1c93858.js",
    "revision": "e960e261760e3c28a574ea00454ed8c2"
  },
  {
    "url": "assets/js/44.b3c56ccf.js",
    "revision": "baadc2950734275e46234e657686d102"
  },
  {
    "url": "assets/js/45.15a2030e.js",
    "revision": "4bb7098a3061c04c511000b535d8cedd"
  },
  {
    "url": "assets/js/46.b83e6bc5.js",
    "revision": "607c85fd562357fc4f68dcd20f5082b1"
  },
  {
    "url": "assets/js/47.c1fd1dbf.js",
    "revision": "275616b15f03abbdda76f306e1a937f6"
  },
  {
    "url": "assets/js/48.b5afed10.js",
    "revision": "b2d1f6351547d125f555a1130111cc78"
  },
  {
    "url": "assets/js/49.859d5923.js",
    "revision": "c7e1d36f16d6336ac5c00ed451a7000e"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.4aa6d10b.js",
    "revision": "ad61e8f52422e919ae392285624d6478"
  },
  {
    "url": "assets/js/51.7bd2bfd6.js",
    "revision": "db9d5aadc98cac8db895701cde4f3c27"
  },
  {
    "url": "assets/js/52.ffb46597.js",
    "revision": "6bb3f66e4f59937d007b587a3aa66b54"
  },
  {
    "url": "assets/js/53.c178ea0c.js",
    "revision": "5fde367c3f02952e19cdaafa1608627f"
  },
  {
    "url": "assets/js/54.ec271ae4.js",
    "revision": "5e02e2ff072438d1c13a2edaf7a29aa2"
  },
  {
    "url": "assets/js/55.a0e76e25.js",
    "revision": "a157213ba2cc86898a4d7ae525da5d0f"
  },
  {
    "url": "assets/js/56.b96e8313.js",
    "revision": "c32e900042035be340dd2f6e600f4dfd"
  },
  {
    "url": "assets/js/57.518fc23c.js",
    "revision": "1e3f750d87f2e6f831a852c459550807"
  },
  {
    "url": "assets/js/58.75a46aef.js",
    "revision": "46850698ce5c160671586c730885e926"
  },
  {
    "url": "assets/js/59.d592c935.js",
    "revision": "1a9a817b55bff2e4d7446c4bb0e00230"
  },
  {
    "url": "assets/js/6.9b196c0a.js",
    "revision": "51734bd22d15cde4738a43b0df3f10e4"
  },
  {
    "url": "assets/js/60.f768ea29.js",
    "revision": "49bc19716fad9bd1faa664dd5e590dbb"
  },
  {
    "url": "assets/js/61.540ac807.js",
    "revision": "1bc13e724c5c263b0d00bdc5d6bc22b8"
  },
  {
    "url": "assets/js/62.8c6381a8.js",
    "revision": "8871fd5da8db36f651c478aa7ae6ebba"
  },
  {
    "url": "assets/js/63.8d5d5090.js",
    "revision": "71faef07087d1d5a011154f5305902c2"
  },
  {
    "url": "assets/js/64.e7d9ef20.js",
    "revision": "c2e0edf11f6261404522163b0529d364"
  },
  {
    "url": "assets/js/65.959244b0.js",
    "revision": "56efeeeaafa9fc7a4e84202432e70c1e"
  },
  {
    "url": "assets/js/66.8ec657d0.js",
    "revision": "34791dfbfb875fd618767557b63ac840"
  },
  {
    "url": "assets/js/67.523c436f.js",
    "revision": "4932efdd9dd81a606a4022aff00896ac"
  },
  {
    "url": "assets/js/68.8e4e5378.js",
    "revision": "f2797bfe2df365cb9ea55e5428f642d3"
  },
  {
    "url": "assets/js/69.e23e33ed.js",
    "revision": "2b35fc2e456dab8baeda9eac25a84fae"
  },
  {
    "url": "assets/js/7.7714163a.js",
    "revision": "bf8a3e825877530cc1dd10cc1d96161a"
  },
  {
    "url": "assets/js/70.82be60ab.js",
    "revision": "246fb3da230034c08034c94a861e5af7"
  },
  {
    "url": "assets/js/71.9e525814.js",
    "revision": "00332973cde050b557326481dcef9b9e"
  },
  {
    "url": "assets/js/72.7025bd53.js",
    "revision": "8316225dc2e63039d13efd495d2cef16"
  },
  {
    "url": "assets/js/73.1c7c6287.js",
    "revision": "78dc81d7a6f98b1afb556364b6db8c94"
  },
  {
    "url": "assets/js/74.17a1eccc.js",
    "revision": "17ea52093d6abec1e31b167803e8724b"
  },
  {
    "url": "assets/js/75.b4e4e720.js",
    "revision": "898de70a8d8ac0c65ee884a721c06893"
  },
  {
    "url": "assets/js/76.b944c7cc.js",
    "revision": "8f9f6af4e47a1630917d3f2551570f8e"
  },
  {
    "url": "assets/js/77.23b62736.js",
    "revision": "3fc3687a6c1b9342be52ba45e7fc0bc2"
  },
  {
    "url": "assets/js/78.89d0baaf.js",
    "revision": "490dff026ed1799ee45442104cafee22"
  },
  {
    "url": "assets/js/79.cab7a1cc.js",
    "revision": "07d10aa440ad567bd89ca4433ecc651a"
  },
  {
    "url": "assets/js/8.00df56a7.js",
    "revision": "d9c1f86abf6302ae7593fe833e1326f8"
  },
  {
    "url": "assets/js/80.3cabcb28.js",
    "revision": "d9f19d59929a7ef59b2989f128548769"
  },
  {
    "url": "assets/js/81.5ea11217.js",
    "revision": "4e60d07fe1be4a00bd660d4132408e6c"
  },
  {
    "url": "assets/js/82.11c6c075.js",
    "revision": "6ba5116b31cdbfbb530eca5f7d352592"
  },
  {
    "url": "assets/js/83.95a07895.js",
    "revision": "8c46ef0bec04c820a7248b96c09803dd"
  },
  {
    "url": "assets/js/84.6ac0955b.js",
    "revision": "356c57cc839eb250b708ada03e0574c3"
  },
  {
    "url": "assets/js/85.9f554e79.js",
    "revision": "e25587f01b3e08bc36e9794480668f32"
  },
  {
    "url": "assets/js/86.4a8cc6f4.js",
    "revision": "e7493937425f054adef23d3a1e209b9e"
  },
  {
    "url": "assets/js/87.7ca6b686.js",
    "revision": "0ca7f0eb53fb262d483491979a1cd822"
  },
  {
    "url": "assets/js/88.6b83c766.js",
    "revision": "721f1f41a28b2f1bb3ae176baf36a4be"
  },
  {
    "url": "assets/js/89.33970a91.js",
    "revision": "fbe00e1e5ad804cceb0526afde06fbe0"
  },
  {
    "url": "assets/js/9.a0bb1d9b.js",
    "revision": "f26cf94a1ae3f205465accabf034827c"
  },
  {
    "url": "assets/js/90.78215fd5.js",
    "revision": "d54e08adca64296fb69facf29d14b294"
  },
  {
    "url": "assets/js/91.0a5747e4.js",
    "revision": "0971352a736a1851abceb20da608977d"
  },
  {
    "url": "assets/js/92.e0d675e0.js",
    "revision": "710b7f91beae3b7642f4ee28ea3cc944"
  },
  {
    "url": "assets/js/93.2eb269e4.js",
    "revision": "3c67b8084e9f46bfacba845c8f34b40f"
  },
  {
    "url": "assets/js/94.52c96b1c.js",
    "revision": "761bfc77e5cebb5497cd91258142dac0"
  },
  {
    "url": "assets/js/95.676ada40.js",
    "revision": "e5ecdc13f898020c249f46eec08161af"
  },
  {
    "url": "assets/js/96.805ce138.js",
    "revision": "94b233e85072317c26f855911d5cf38d"
  },
  {
    "url": "assets/js/97.0aa1e952.js",
    "revision": "cc38a01f377274d179c78202923ea0b8"
  },
  {
    "url": "assets/js/98.f60a3202.js",
    "revision": "efc99936f3fc190cd1054792f51ffcc4"
  },
  {
    "url": "assets/js/app.8d3625dd.js",
    "revision": "3c795a66e271a40792f91748c8569b38"
  },
  {
    "url": "changelog.html",
    "revision": "1fc006a7c418885e6536775b3c0d32c6"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "2c7da960f2e6a8989d13820b0ac07c46"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "e100cd961e4e4b6041191e86006b8439"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "e13f87b2584a83f9acb84e6cca86d8db"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "15b7f14935afb409e7259e5498c68936"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "71a7512694c0c5d0acb84a3f920aba70"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "2c51cd6e76f2138865956d492be80a09"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "efae9981a52190d046ce533f575f63a3"
  },
  {
    "url": "guide/index.html",
    "revision": "0e9614abf5c227e9dff9cc3c5b09499a"
  },
  {
    "url": "guide/installation.html",
    "revision": "8af9385cb35757bc73756d736ae6876e"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "052681a22afea872896f6321b687af00"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "5058609780f4e1ca379d77175b65772c"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "a2215f647cf019227845c89945cf3eec"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "b2e28a5bab57828f1a91a3e1e8590b37"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "a7ed963e1b13960dee986db7c81a13a1"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "9f2e96df4cb93d7876dd4841caeef4b2"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "11de2af2e6565f7cae5f8cd0c60ac275"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "76d17101af73a969cbf629f2fe305cab"
  },
  {
    "url": "next/api/config.html",
    "revision": "84e4ba3f65081971a4247b8e546e5097"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "1307ce8c13b5ac9ee00b1d5dbbaaa91e"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "1c341ae9ebb7a898764256b0c9747f61"
  },
  {
    "url": "next/api/exception.html",
    "revision": "87be4a79f74aefc6a31374236f560402"
  },
  {
    "url": "next/api/index.html",
    "revision": "4bbf4aadb30a8c4ec39ffb73f0ef36e5"
  },
  {
    "url": "next/api/log.html",
    "revision": "5053d5580a8d838d0d0a98be2e5c4cd5"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "d31571456569173bb2ec308fe1c99de7"
  },
  {
    "url": "next/api/message.html",
    "revision": "56378f5d5eb3935ac0b23d26c022c65b"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "c05b65f386673e8022132ee37009f830"
  },
  {
    "url": "next/api/permission.html",
    "revision": "70976148ecb86755c287f0ebd5a6c9fb"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "547acc73328ac164ec5240fd24105b64"
  },
  {
    "url": "next/api/rule.html",
    "revision": "77e85c427ffcd7a42d29ce6e13bbfc6b"
  },
  {
    "url": "next/api/sched.html",
    "revision": "aa280477549a4b708174ec004da259e1"
  },
  {
    "url": "next/api/typing.html",
    "revision": "86433d35490610aa3534f36e0e7960cf"
  },
  {
    "url": "next/api/utils.html",
    "revision": "c12b04e1b0f0424bd795535e0e6c03ce"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "bd26aa50ba8645dbfafc92a87b80aac1"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "c3f49fb63c0f3929072fc1dde84f27df"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "68bbc703173c60311aef7bd50ff2d8f6"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "19b8377e3a9cbe1071d47a2eb3dbf41e"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "3172df9668fa239185fe1a9004bfcd15"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "d4239b0cfd0b5f5b37ec392dcb576fa8"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "8012a7e58c3d107f1f38431250c9b9dc"
  },
  {
    "url": "next/guide/index.html",
    "revision": "282b7f2ceac2436a289cd245d9ae416f"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "f6bec05fce4c1608a328d433b668ad45"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "12498728d47c3ce2118c631f3f5a0bf1"
  },
  {
    "url": "next/index.html",
    "revision": "eb104aab96c78b368fe1e2a55a518f20"
  },
  {
    "url": "plugin-store.html",
    "revision": "acc6c1d765c95662b3ecb750e8c743d4"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
