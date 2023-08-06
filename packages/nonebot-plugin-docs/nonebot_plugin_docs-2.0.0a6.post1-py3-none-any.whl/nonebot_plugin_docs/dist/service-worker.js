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
    "revision": "f5645ef06e0d202d318e36c66f794b5a"
  },
  {
    "url": "2.0.0a4/api/adapters/index.html",
    "revision": "a22ea099b3db3431ca98304e14f4327a"
  },
  {
    "url": "2.0.0a4/api/config.html",
    "revision": "59539ffd25127c2d57f4a9a6430ba115"
  },
  {
    "url": "2.0.0a4/api/drivers/fastapi.html",
    "revision": "5b66a62fb05c370e4ef06def6c699378"
  },
  {
    "url": "2.0.0a4/api/drivers/index.html",
    "revision": "425ab6ed4925d91e5822eb83a231163a"
  },
  {
    "url": "2.0.0a4/api/exception.html",
    "revision": "2045f88161d69a914a403783ae4bfa62"
  },
  {
    "url": "2.0.0a4/api/index.html",
    "revision": "de387d4637fbef5c9730fd6bc1b37d9f"
  },
  {
    "url": "2.0.0a4/api/log.html",
    "revision": "23831ea214cd145b104216024127d9a7"
  },
  {
    "url": "2.0.0a4/api/matcher.html",
    "revision": "58e04c9fd178b56140ab0264156f30f1"
  },
  {
    "url": "2.0.0a4/api/nonebot.html",
    "revision": "8b6942539a434efabcd96092a0b646c7"
  },
  {
    "url": "2.0.0a4/api/permission.html",
    "revision": "29bcd1f6b121730ab87eb9c459d47e65"
  },
  {
    "url": "2.0.0a4/api/plugin.html",
    "revision": "d7728903e6915b1ce7f52c1d703c6faf"
  },
  {
    "url": "2.0.0a4/api/rule.html",
    "revision": "dbe45bcd5c29edcfe6b094c51119d459"
  },
  {
    "url": "2.0.0a4/api/sched.html",
    "revision": "223140b341518e3791dddcca5b52cf01"
  },
  {
    "url": "2.0.0a4/api/typing.html",
    "revision": "709638c4c2019bcd44a08b0cc4b8ae05"
  },
  {
    "url": "2.0.0a4/api/utils.html",
    "revision": "2947fe480dff46cff46568374f385a8e"
  },
  {
    "url": "2.0.0a4/guide/basic-configuration.html",
    "revision": "494f7a981eaa3e55b7f44dd03db94158"
  },
  {
    "url": "2.0.0a4/guide/creating-a-project.html",
    "revision": "ed2e74c6008293f8196285375e30c3f2"
  },
  {
    "url": "2.0.0a4/guide/getting-started.html",
    "revision": "e5af47fccea2e59a49e103aba2fab886"
  },
  {
    "url": "2.0.0a4/guide/index.html",
    "revision": "9040d960c72ad83b082258ac84914174"
  },
  {
    "url": "2.0.0a4/guide/installation.html",
    "revision": "9cdce4e7ba0021f8541f63a0fad2feff"
  },
  {
    "url": "2.0.0a4/guide/writing-a-plugin.html",
    "revision": "786889d5ec0814e45a9014e9f4679ab4"
  },
  {
    "url": "2.0.0a4/index.html",
    "revision": "943798648a50ee4badf8b8fa4b4a43c7"
  },
  {
    "url": "404.html",
    "revision": "5e0484adee65a34c634141b71a06d316"
  },
  {
    "url": "advanced/index.html",
    "revision": "8d337608c0f4fc7a91fd7d61953f4cc0"
  },
  {
    "url": "advanced/permission.html",
    "revision": "f592518012b4a3931533a0783432f3da"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "47df36741be9a91232b833f23b744add"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "c2ea74bc5efd63fe3103d95b5f72de98"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "c34de4ea25691edb40fc588b9058f32e"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "9d9e4b091b4db6db0f9dca67a4b0934e"
  },
  {
    "url": "api/config.html",
    "revision": "56c615d9a6eeab25ea8a9b52a2cc44a1"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "409bb2459dc8a518532a30560320d4c2"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "12a4ef5edd8a92e527264b6cf3f753d6"
  },
  {
    "url": "api/exception.html",
    "revision": "c58c255a881f7a76cb1d515ec5330f85"
  },
  {
    "url": "api/index.html",
    "revision": "2df02059fccbb32075a11c99cd96f90a"
  },
  {
    "url": "api/log.html",
    "revision": "dcb845ac7d9bfa2e3c52938e844dc079"
  },
  {
    "url": "api/matcher.html",
    "revision": "515f3c72c3561d5a27fe160401f27e54"
  },
  {
    "url": "api/message.html",
    "revision": "5cbe5ba848662574a3c934c7a8b90f26"
  },
  {
    "url": "api/nonebot.html",
    "revision": "ab2c73126f6708a3cc1d4f0e0ad86f7a"
  },
  {
    "url": "api/permission.html",
    "revision": "0555580a0ad872b7bde3e314dce19b29"
  },
  {
    "url": "api/plugin.html",
    "revision": "d97ebb26c1605c2bb6b2b06920626ad7"
  },
  {
    "url": "api/rule.html",
    "revision": "b9cbeee2663f39d913c3314d65b3168d"
  },
  {
    "url": "api/sched.html",
    "revision": "5e59180a4081649e43b2acabbb0d6b9e"
  },
  {
    "url": "api/typing.html",
    "revision": "113e1740aa912d464a50fef5b3fa909d"
  },
  {
    "url": "api/utils.html",
    "revision": "e68d1d4b749fd2691bd8ff2a43380102"
  },
  {
    "url": "assets/css/0.styles.b5bcb7cc.css",
    "revision": "462d2aeec3bb45377259af631cd4bb8b"
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
    "url": "assets/js/10.b92fc5f9.js",
    "revision": "8c904ba1303a572bacead497c67ce9fe"
  },
  {
    "url": "assets/js/11.a726cc71.js",
    "revision": "60c1e819071bf7298abeb2c0fbdfe9cb"
  },
  {
    "url": "assets/js/12.7cc9ee3a.js",
    "revision": "544c69156d49e3178642c243a3e92ca4"
  },
  {
    "url": "assets/js/13.87b28af3.js",
    "revision": "7c744b595faf74ba434c910240ea07c4"
  },
  {
    "url": "assets/js/14.2f0f00f0.js",
    "revision": "b9182cc045e7dcab3cd61bfd988d1eb6"
  },
  {
    "url": "assets/js/15.c596f4aa.js",
    "revision": "646d77d7b9f74b223f6c0521b3c28704"
  },
  {
    "url": "assets/js/16.06752651.js",
    "revision": "c5b24a2261e4eb9daf8a98e151aeecf9"
  },
  {
    "url": "assets/js/17.de1be4f4.js",
    "revision": "539677ac4ad453f0a64780a82288a5ec"
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
    "url": "assets/js/21.f617522b.js",
    "revision": "e002dd5e21114d99ffc5c618bce4cae0"
  },
  {
    "url": "assets/js/22.b077e96e.js",
    "revision": "9b7f3e5127f4afae9f058ff768a7fcc3"
  },
  {
    "url": "assets/js/23.1147b189.js",
    "revision": "77b59f4a86a13bb9fa3b17b942675458"
  },
  {
    "url": "assets/js/24.472cafc5.js",
    "revision": "da5ca822bbd74762cca3667bdccca691"
  },
  {
    "url": "assets/js/25.f676453e.js",
    "revision": "842a8169f60fced23540ca934e827b46"
  },
  {
    "url": "assets/js/26.4b935a4d.js",
    "revision": "d44980941e69242080a1b2b9fd003b30"
  },
  {
    "url": "assets/js/27.38999ad6.js",
    "revision": "d1b8fa53366cad9dff5b173797f39138"
  },
  {
    "url": "assets/js/28.610ae5ee.js",
    "revision": "e8c2dc948ef5f5f72bb09c17f0f98c6a"
  },
  {
    "url": "assets/js/29.f7cb36d9.js",
    "revision": "9e53401ab4e48506620d0e89f3c4c95b"
  },
  {
    "url": "assets/js/3.4bfdb268.js",
    "revision": "117b26248350caf0435164fb2ee00b08"
  },
  {
    "url": "assets/js/30.1fb45fb4.js",
    "revision": "c62ef93624d1b4f7301362af4199bb96"
  },
  {
    "url": "assets/js/31.ecc38ca0.js",
    "revision": "98e415e9cdc12c43b6d0399b9f08a41d"
  },
  {
    "url": "assets/js/32.47065d2b.js",
    "revision": "db99b31f010ec674cc25dd4635336b36"
  },
  {
    "url": "assets/js/33.51813198.js",
    "revision": "44cd0ae4e7b8d3f06fa380da94125d42"
  },
  {
    "url": "assets/js/34.de92d48b.js",
    "revision": "a2291eaf787a5071e931e18f1b4528c9"
  },
  {
    "url": "assets/js/35.d88de6dc.js",
    "revision": "971c753db3181ff36dc504dbbcc97710"
  },
  {
    "url": "assets/js/36.3e266698.js",
    "revision": "b4d3241a38ebb26f7772f20670cdabcc"
  },
  {
    "url": "assets/js/37.df0590cf.js",
    "revision": "81b0a8694ae4b991141f22b72d9fb50d"
  },
  {
    "url": "assets/js/38.b8f4a5e9.js",
    "revision": "5805b2d2602fc4653f9834674f229396"
  },
  {
    "url": "assets/js/39.72befae2.js",
    "revision": "7f02185815abebe89c6e3c317c35f342"
  },
  {
    "url": "assets/js/4.fefb5760.js",
    "revision": "f9c6601b542c55dd38c610ffd6f585a2"
  },
  {
    "url": "assets/js/40.c4567017.js",
    "revision": "5298bc2b38c268cff14eb33cafa26187"
  },
  {
    "url": "assets/js/41.6bac1e1f.js",
    "revision": "1f60fba1702eaa59967bc01228e1cb67"
  },
  {
    "url": "assets/js/42.3c309f62.js",
    "revision": "c74665b62139e706e5b66813f927a682"
  },
  {
    "url": "assets/js/43.e03048c2.js",
    "revision": "23d34e769bf16be6003d5779d730b88d"
  },
  {
    "url": "assets/js/44.c41c8f7f.js",
    "revision": "ca6850cf8496de26481ae2a7ea281c12"
  },
  {
    "url": "assets/js/45.0f4d7f66.js",
    "revision": "2b5aa6dcac13a4caa05cfcfeb86f93dd"
  },
  {
    "url": "assets/js/46.9ed9ff2f.js",
    "revision": "772f22e2c4ecd5ab965f8eb9bc18c733"
  },
  {
    "url": "assets/js/47.ec232400.js",
    "revision": "fa0c2f21876748eb336d356ccdbd2595"
  },
  {
    "url": "assets/js/48.87d5a160.js",
    "revision": "ed70ab819ec6d80420527c8b473b79da"
  },
  {
    "url": "assets/js/49.773b38f1.js",
    "revision": "a18ec429a15ecfb11716d7310735be1a"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.75b77afb.js",
    "revision": "5830abe540ee31aa6f0d305c93d26f29"
  },
  {
    "url": "assets/js/51.0146670a.js",
    "revision": "7edbf26cf132c1e80db52b88dc1714a5"
  },
  {
    "url": "assets/js/52.ffb46597.js",
    "revision": "6bb3f66e4f59937d007b587a3aa66b54"
  },
  {
    "url": "assets/js/53.2f518a3b.js",
    "revision": "12b9b40924758b3bb6d61f890d9df2c7"
  },
  {
    "url": "assets/js/54.760be085.js",
    "revision": "8a58f7e54a872d67aaf8e415470847f3"
  },
  {
    "url": "assets/js/55.a0e76e25.js",
    "revision": "a157213ba2cc86898a4d7ae525da5d0f"
  },
  {
    "url": "assets/js/56.760dbc95.js",
    "revision": "e156d58be87c2357840b8a974c6cc617"
  },
  {
    "url": "assets/js/57.592f0df9.js",
    "revision": "e0321ea22cf411550800e051220fd268"
  },
  {
    "url": "assets/js/58.af43b231.js",
    "revision": "90a1a544a635a3884327efe8ec727cae"
  },
  {
    "url": "assets/js/59.c5804f11.js",
    "revision": "18f4a22d2f7a3d9c3d203ccac8a07b86"
  },
  {
    "url": "assets/js/6.9b196c0a.js",
    "revision": "51734bd22d15cde4738a43b0df3f10e4"
  },
  {
    "url": "assets/js/60.6808e3a4.js",
    "revision": "a86228752ae3fbd125ac8eed9be17af9"
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
    "url": "assets/js/63.8663abe8.js",
    "revision": "da14e8c9252f5a325849c15a4ba745d6"
  },
  {
    "url": "assets/js/64.9684f8dc.js",
    "revision": "e244c102eaac3a0fe817cad92aeaeaba"
  },
  {
    "url": "assets/js/65.8a9ac285.js",
    "revision": "32cf33b3e700cad55a9d40e61e24da28"
  },
  {
    "url": "assets/js/66.8259cbc4.js",
    "revision": "72207093482c6aa6eca9e9640531a177"
  },
  {
    "url": "assets/js/67.92401849.js",
    "revision": "3057a27e3ad27f5be2f5837813046a86"
  },
  {
    "url": "assets/js/68.6dc82220.js",
    "revision": "7eafd69d6852d23c17f0ab29b3a8725d"
  },
  {
    "url": "assets/js/69.b6a16273.js",
    "revision": "582a1e8e8963dcb0ab6fe0ae1bcb0d7d"
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
    "url": "assets/js/73.38385aa0.js",
    "revision": "81423747cf7044b01df0333fc44e6e18"
  },
  {
    "url": "assets/js/74.d7ad41fd.js",
    "revision": "d78ec60ccb9fdb6e1ecf62e463db0dc6"
  },
  {
    "url": "assets/js/75.1efa42e3.js",
    "revision": "294800533906cc6dd362281016d1477a"
  },
  {
    "url": "assets/js/76.a9b4b039.js",
    "revision": "fb213ac2a4c6a5e6addd4626cc9fa035"
  },
  {
    "url": "assets/js/77.7bcc1da3.js",
    "revision": "3a54e86b1a7d37e1aaa95568d792928b"
  },
  {
    "url": "assets/js/78.4ed6359f.js",
    "revision": "ab93c63e1c8592cbbbf2a3b5adef285a"
  },
  {
    "url": "assets/js/79.f2473da0.js",
    "revision": "fdb2715ffa2b8607c3c5d2c9955372b3"
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
    "url": "assets/js/81.1bf08edf.js",
    "revision": "b401ccdaedb0627f52c4ea89a280a959"
  },
  {
    "url": "assets/js/82.6f9b38e1.js",
    "revision": "94969fdb3bce9bf25c3ab53b43a3fb28"
  },
  {
    "url": "assets/js/83.cd0b2f52.js",
    "revision": "43b0d1896327dc01739c120657f1773e"
  },
  {
    "url": "assets/js/84.e34af6ca.js",
    "revision": "d0c2f93448bf3e480156c4414f4756d3"
  },
  {
    "url": "assets/js/85.132029c9.js",
    "revision": "422198ac410a982313447f1827801616"
  },
  {
    "url": "assets/js/86.d849b170.js",
    "revision": "851dc8b8fc73103499c10b48c23ee8b3"
  },
  {
    "url": "assets/js/87.742b784e.js",
    "revision": "e89342c744e1328a2917714709e3e869"
  },
  {
    "url": "assets/js/88.a5a47095.js",
    "revision": "601b3123e5f9c34cb715428f1ffe4df5"
  },
  {
    "url": "assets/js/89.33970a91.js",
    "revision": "fbe00e1e5ad804cceb0526afde06fbe0"
  },
  {
    "url": "assets/js/9.9396fa5f.js",
    "revision": "3788e5e1124a3c55693ab5c6c096348a"
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
    "url": "assets/js/93.1b2d6b90.js",
    "revision": "df14bcfcd4c45fa8092d58c79071addc"
  },
  {
    "url": "assets/js/94.9c80c8bf.js",
    "revision": "f8cc1bacce28306704e281d814ffaff9"
  },
  {
    "url": "assets/js/95.676ada40.js",
    "revision": "e5ecdc13f898020c249f46eec08161af"
  },
  {
    "url": "assets/js/96.a120c9dc.js",
    "revision": "d1244dfa3cb98025957d27d893f5caef"
  },
  {
    "url": "assets/js/97.ccf7fa0e.js",
    "revision": "255fddf19a67322f116ffaca3b8c02eb"
  },
  {
    "url": "assets/js/98.f60a3202.js",
    "revision": "efc99936f3fc190cd1054792f51ffcc4"
  },
  {
    "url": "assets/js/app.73ad14ce.js",
    "revision": "59f1d971e6c9da1614762d6a7a7d8dfc"
  },
  {
    "url": "changelog.html",
    "revision": "60cac0b307a0b74c1e17606ae633fd0f"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "7ecbf683f24d6b2294ff9a57e86f39ba"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "832beff91e8f7dcbc2ec2e85bb51c744"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "437ca5f59859ea4effac1330e26eae79"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "c4a8ac68db5727de7104f61bd54757a8"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "765343a285dd95caec8db122cbff9967"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "e3ac5dbe8b7bb83028b29711241786e5"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "351293cbd3af9d66007c9848e7d7850a"
  },
  {
    "url": "guide/index.html",
    "revision": "aeb602bba9e57573f4d340584f8ecc3f"
  },
  {
    "url": "guide/installation.html",
    "revision": "2189677aa0534ad18c2fa84a392b18c6"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "cf5a5209f9cc3f201b1ee4a10dc03e28"
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
    "revision": "f47d921638d41651da7d0d7ed6d99b25"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "cc9ef87e759eb7fb55dfd590ecc83603"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "1b446dae25e14249552cfe5ede5000ee"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "95f9645c5921dcd150ac4af5477983a2"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "7b4131c6dfc7e2d4164fa2c98f04fe9a"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "c7b6efa3a1120b76d184ebd97ab5a41d"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "1ead1242ec322c886efa8a6cf55526cc"
  },
  {
    "url": "next/api/config.html",
    "revision": "12e77a6f479b0fc773e30cb2840deea5"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "b2b67240fa821c6519217240e5e38640"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "bdb7a7a2300440252ce287c0ef6c28d4"
  },
  {
    "url": "next/api/exception.html",
    "revision": "2e46b32eabfb756ee31cffc7f8458aa6"
  },
  {
    "url": "next/api/index.html",
    "revision": "e83bcbec2c2401e12c66958bb27c02af"
  },
  {
    "url": "next/api/log.html",
    "revision": "9fa36cd6354120abe72aaa856eb8e8f6"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "fdbfa11121a7b1933e3c2bbff5fc66fa"
  },
  {
    "url": "next/api/message.html",
    "revision": "9805d4fefe002e72f0803a3f4d3f0ae0"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "67db8e2f4b36e949614786923a0a3a75"
  },
  {
    "url": "next/api/permission.html",
    "revision": "6d19e8384748191c5510241fa8a17b21"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "a6ea38ccf6ddcaccd006a4b2290ca313"
  },
  {
    "url": "next/api/rule.html",
    "revision": "52f7ab780ecc6ae92dfea98a6a6548aa"
  },
  {
    "url": "next/api/sched.html",
    "revision": "3964a7addfbb80ec6f2aa4ac87a7661c"
  },
  {
    "url": "next/api/typing.html",
    "revision": "999aad1dce25f8573b827d0ac93ba43f"
  },
  {
    "url": "next/api/utils.html",
    "revision": "03087822a7cac5ebecda5d9bfadd06ae"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "8120d29a9ddeccf75e7a8b234b259d63"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "d6e93411be5cd254d775422d35c4e4e0"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "629edf42b365a66fcf451fd72a0a7676"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "0bb002cfc699448470668b82dfd4a000"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "c886ae1db6f876cea3ef329dc843bea9"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "9d2a01ba987bec8f2592a8480dd7108a"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "560ab64d9bc8b41ff9bd82f2ca96d986"
  },
  {
    "url": "next/guide/index.html",
    "revision": "41d5020c882ea5d3ea46b19aa6f46660"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "e771d0941622710bdaf93d472a075b07"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "6e914da638b05565fa935bcb909955e2"
  },
  {
    "url": "next/index.html",
    "revision": "10aaaa85f617a031c580bfcac77ba0be"
  },
  {
    "url": "plugin-store.html",
    "revision": "d664d0fda3764c3c73d03c9ce5e936f9"
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
