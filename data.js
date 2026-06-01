// ── DIVISION GLOBAL — DATA ──────────────────────────────────────────

const FEATURED_PROJECTS = [
  { client: "Hublot", title: "FW25", slug: "hublot", tags: ["VFX"], role: "VFX", image: "assets/projects/HUBLOT%20-%20FW25/PREVIEW/DUO%20XXL%20FOR%20INSTA%20WITH%20COVER_10.webp", video: "assets/projects/HUBLOT%20-%20FW25/VIDEO/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2004%20-%2016x9_1.mp4", videos: ["assets/projects/HUBLOT%20-%20FW25/VIDEO/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2004%20-%2016x9_1.mp4", "assets/projects/HUBLOT%20-%20FW25/VIDEO/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2002%20-%2016x9_1.mp4", "assets/projects/HUBLOT%20-%20FW25/VIDEO/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2001%20-%2016x9_1.mp4"], year: "2026", description: "Hublot FW25 directed by Nolann Blettner Romain Abboud, produced by Vanta\nDOP Cyan Mariani\nVFX supervisor  Nolann Blettner\nCompositing Jonathan Truong & Noémie Ducly\n3D Generalist  Antoine Danion Valentin Gaubert", wips: ["assets/projects/HUBLOT%20-%20FW25/WIP/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2004%20-%2016x9_1.mp4", "assets/projects/HUBLOT%20-%20FW25/WIP/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2002%20-%2016x9_1.mp4", "assets/projects/HUBLOT%20-%20FW25/WIP/WINTER%20CAMPAIGN%202025%20-%20LS%20-%20LOOP%2001%20-%2016x9_1.mp4"] },
  { client: "Graduation Project", title: "To Make, Metal", slug: "to-make-metal", tags: ["Creative Direction", "CGI"], role: "Creative Direction, CGI", image: "assets/projects/TO%20MAKE%20-%20METAL/PREVIEW/1.png", video: "assets/projects/TO%20MAKE%20-%20METAL/VIDEO/tomake_sq01_METAL_master_v01_1.mp4", year: "2025", description: "\"TO MAKE\" is a fictional media project designed to showcase fine craftsmanship through material-led visual experiments.\nHere is some CGI experiments I've made around METAL.CGI by Noémie Ducly, concept with MARIUS GIRAUDET and sound design by BASIL NOORDANUS-CALMELS", wips: ["assets/projects/TO%20MAKE%20-%20METAL/WIP/1.jpg", "assets/projects/TO%20MAKE%20-%20METAL/WIP/2.jpg", "assets/projects/TO%20MAKE%20-%20METAL/WIP/3.jpg", "assets/projects/TO%20MAKE%20-%20METAL/WIP/5.jpg", "assets/projects/TO%20MAKE%20-%20METAL/WIP/6.jpg", "assets/projects/TO%20MAKE%20-%20METAL/WIP/7.mp4"] },
  { client: "Graduation Project", title: "To Make, Minerals", slug: "to-make-minerals", tags: ["Creative Direction", "CGI"], role: "Creative Direction, CGI", image: "assets/projects/TO%20MAKE%20-%20MINERALS/PREVIEW/Still%202026-01-20%20094819_1.4.1.png", video: "assets/projects/TO%20MAKE%20-%20MINERALS/VIDEO/tomake_pierre_master.mp4", year: "2025", description: "\"TO MAKE\" is a fictional media project designed to showcase fine craftsmanship through material-led visual experiments.\nHere is some CGI experiments I've made around MINERALS. CGI by Noémie Ducly, concept with MARIUS GIRAUDET and sound design by BASIL NOORDANUS-CALMELS", wips: ["assets/projects/TO%20MAKE%20-%20MINERALS/WIP/2.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/3.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/8.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/10.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/11.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/12.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/Still%202026-01-19%20153646_2.4.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/Still%202026-01-19%20171419_4.1.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/Still%202026-01-19%20171440_2.3.jpg", "assets/projects/TO%20MAKE%20-%20MINERALS/WIP/Still%202026-01-20%20094819_1.4.jpg"] },
  { client: "Graduation Project", title: "To Make, Pigments", slug: "to-make-pigments", tags: ["Creative Direction", "CGI"], role: "Creative Direction, CGI", image: "assets/projects/TO%20MAKE%20-%20PIGMENTS/PREVIEW/Still%202026-01-19%20153646_4.4.1.png", video: "assets/projects/TO%20MAKE%20-%20PIGMENTS/VIDEO/tomake_sq08_master_v07.mp4", year: "2025", description: "\"TO MAKE\" is a fictional media project designed to showcase fine craftsmanship through material-led visual experiments.\nHere is some CGI and AI experiments I've made around pigments. CGI by NOEMIE DUCLY and sound design by BASIL NOORDANUS-CALMELS", wips: ["assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/PIGMENT_v02_1.jpg", "assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/Still%202026-01-19%20153646_3.9.jpg", "assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/Still%202026-01-19%20153646_4.4.jpg", "assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/Still%202026-01-19%20155215_3.10.jpg", "assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/Still%202026-01-19%20155334_4.3.jpg", "assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/Still%202026-01-19%20170706_3.2.jpg", "assets/projects/TO%20MAKE%20-%20PIGMENTS/WIP/tomake_sq08_pigment_cut%204_master_v01.mp4"] },
  { client: "Graduation Project", title: "To Make, Wood", slug: "to-make-wood", tags: ["Creative Direction", "CGI"], role: "Creative Direction, CGI", image: "assets/projects/TO%20MAKE%20-%20WOOD/PREVIEW/Still%202026-01-19%20153646_3.1.1.png", video: "assets/projects/TO%20MAKE%20-%20WOOD/VIDEO/tomake_bois_1.mp4", year: "2025", description: "\"TO MAKE\" is a fictional media project designed to showcase fine craftsmanship through material-led visual experiments.\nHere is some CGI and AI experiments I've made around WOOD. CGI by NOEMIE DUCLY, concept with MARIUS GIRAUDET and sound design by BASIL NOORDANUS-CALMELS", wips: ["assets/projects/TO%20MAKE%20-%20WOOD/WIP/Still%202026-01-19%20153646_2.1.jpg", "assets/projects/TO%20MAKE%20-%20WOOD/WIP/Still%202026-01-19%20153646_2.2.jpg", "assets/projects/TO%20MAKE%20-%20WOOD/WIP/Still%202026-01-19%20153646_3.1.jpg", "assets/projects/TO%20MAKE%20-%20WOOD/WIP/Still%202026-01-19%20155842_3.2.jpg", "assets/projects/TO%20MAKE%20-%20WOOD/WIP/Still%202026-01-19%20161520_2.5.jpg"] },
  { client: "Amelia Dimoldenberg", title: "Chicken Shop Date", slug: "chicken-shop-date", tags: ["Creative Direction", "CGI"], role: "Creative Direction, CGI", image: "assets/projects/CHICKENSHOPDATE/PREVIEW/Still%202026-04-16%20013050_2.2.8.jpg", video: "assets/projects/CHICKENSHOPDATE/VIDEO/ChickenShopDate_g%C3%A9n%C3%A9rique_1.mp4", year: "2025", description: "Fictional title sequence project for Chicken Shop Date interviews by Amelia Dimoldenberg.\nConcept with THOMAS DI SCALA\nDirection, CGI and compositing by NOEMIE DUCLY\nAnimation by THOMAS DI SCALA.", wips: ["assets/projects/CHICKENSHOPDATE/WIP/BREAKDOWN_01_1.mp4", "assets/projects/CHICKENSHOPDATE/WIP/Still%202026-04-16%20012939_2.2.1.jpg", "assets/projects/CHICKENSHOPDATE/WIP/Still%202026-04-16%20012939_2.2.12.jpg", "assets/projects/CHICKENSHOPDATE/WIP/Still%202026-04-16%20012939_2.2.4.jpg", "assets/projects/CHICKENSHOPDATE/WIP/Still%202026-04-16%20012939_2.2.5.jpg", "assets/projects/CHICKENSHOPDATE/WIP/Still%202026-04-16%20012939_2.2.9.jpg"] },
  { client: "Mugler", title: "Les Exceptions", slug: "les-exceptions", tags: ["Creative Direction", "CGI"], role: "Creative Direction, CGI", image: "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/PREVIEW/Still%202026-04-17%20015455_1.15.1.jpg", video: "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/VIDEO/MUGLER_G_CYAN_1_1.mp4", year: "2026", description: "Fictional teaser project inspired by Mugler's fashion show, created for the Les Exceptions fragrance line.\nConcept by NOEMIE DUCLY,  FARIC CHEN, THOMAS DI SCALA.\nCGI by FARIC CHEN\nCompositing & grade by NOEMIE DUCLY\nMusic: Grief Seed by Lili Castiglioni.", wips: ["assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171241_1.9.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171241_1.11.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171241_2.1.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171241_2.1.2.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.1.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.2.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.4.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.5.2.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.6.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.7.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.8.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171316_1.10.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171331_1.17.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171343_1.17.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171603_1.15.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-20%20171727_1.12.2.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-17%2002.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-17%20023154_1.5.1.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-17%20023154_1.14.2.jpg", "assets/projects/MUGLER%20-%20LES%20EXCEPTIONS/WIP/Still%202026-04-17%20023154_1.14.3.jpg"] },
  { client: "Undercover, Salomon, Footlocker", title: "Off The Room 2", slug: "off-the-room-2", tags: ["CGI"], role: "Motion Design, CGI", image: "assets/projects/OFF%20THE%20ROOM/PREVIEW/PROJET%20J.png", video: "assets/projects/OFF%20THE%20ROOM/VIDEO/FISHEYE%20DJ11_1.mp4", videos: ["assets/projects/OFF%20THE%20ROOM/VIDEO/FISHEYE%20DJ11_1.mp4", "assets/projects/OFF%20THE%20ROOM/VIDEO/LARGE%20H%20DJ11_2.mp4"], year: "2025", description: "Undercover powered by Salomon & Footlocker, 270° MOTION VISUALS\nAD @call.coal @alyasmusic @mickael.azules, directed by @stubroy,\nMotion graphics, CGI made with DISGUYS", wips: ["assets/projects/OFF%20THE%20ROOM/WIP/12MM%20DJ11.mp4"] },
  { client: "YVNNIS, So La Lune", title: "Mal Aimés", slug: "mal-aimes", tags: ["VFX"], role: "VFX, CGI", image: "assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/PREVIEW/MAL_AIMES_GRADE_prores%20v2.00_01_32_23.Still006.jpg", video: null, vimeoUrl: "https://vimeo.com/1154316162", year: "2025", description: "Music video for Yvnnis and So La Lune\nDirected by Nolann Blettner\nCreative Direction : Roy Foo Tam Fong, Léonard Mariotte\nPost-production : DISGUYS\nVFX Supervision : Léonard Mariotte\nCG Generalist : @yass.vfx @antoinedanion @noemieducly & @thomasunderinspo", wips: ["assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/0.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/1.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/2.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/4.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/5.mp4","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/6.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/7.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/8.mp4","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/10.jpg","assets/projects/YVNNIS%20AND%20SO%20LA%20LUNE%20-%20MAL%20AIMES/WIP/11.jpg"] },
  { client: "Graduation Project", title: "To Make, Prints", slug: "to-make-prints", tags: ["Graphic Design"], role: "Graphic Design", image: "assets/projects/TO%20MAKE%20-%20PRINTS/PREVIEW/1.jpg", video: null, year: "2025", description: "\"TO MAKE\" is a fictional media project designed to showcase fine craftsmanship through material-led visual experiments.\n\nA SERIE OF PRINTS CREATED FOR « TO MAKE ».\nBook, 280 × 353 mm, 116 pages\n16 cards, 148 x 105 mm, 75 copies\n\nCGI and graphic design by NOEMIE DUCLY\nConcept and writing with MARIUS GIRAUDET\nBook and cards design by me", wips: ["assets/projects/TO%20MAKE%20-%20PRINTS/WIP/1.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/2.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/3.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/4.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/5.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/6.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/7.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/7aaaaa.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/9.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/10.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/12.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/A.jpg", "assets/projects/TO%20MAKE%20-%20PRINTS/WIP/B.jpg"], wipContain: true },
  { client: "Jolagreen, Tiakola", title: "Locked Up", slug: "locked-up", tags: ["Photography"], role: "Photography", image: "assets/projects/JOLGREEN%20AND%20TIAKOLA/PREVIEW/Frame%20140.jpg", video: null, slides: ["assets/projects/JOLGREEN%20AND%20TIAKOLA/VIDEO/Frame%2080.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/VIDEO/Frame%20100.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/VIDEO/Frame%20120.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/VIDEO/Frame%20140.jpg"], wipInstant: true, wipRatio: "5/4", wipShuffle: true, year: "2026", description: "Pictures and videos from the set of the 'LOCKED UP' music video, directed by Nolann Blettner, Roy Foo Tam Fong, and L\u00e9onard Mariotte.\nDOP Thomas Cazottes, Stylist Tiakola : @djibbzz, Stylist Jolagreen23 : @yannweber", wipShuffle: true, wips: ["assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%206.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%207.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%208.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2010.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2012.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2014.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2021.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2022.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2028.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2032.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2034.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/Frame%2036.jpg","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/JOLATIAKO_camescope_edit_video_v01_00000301_1.mp4","assets/projects/JOLGREEN%20AND%20TIAKOLA/WIP/JOLATIAKO_camescope_edit_video_v01_00000651_1.mp4"] },
];

const DIRECTORS = [
  {
    slug: "alma-de-ricou-and-manon-engel",
    name: "Alma de Ricou & Manon Engel",
    categories: ["Fashion Films", "Photography"],
    tags: ["Film", "Photo"],
    localVideo: "assets/tomake_TEXTILE.mp4",
    projects: [
      { client: "Balenciaga", title: "Campaign 2024", slug: "balenciaga-2024", type: "video", category: "Fashion Films" },
      { client: "Saint Laurent", title: "Short Film", slug: "saint-laurent-short", type: "video", category: "Fashion Films" },
      { client: "Loewe", title: "Editorial", slug: "loewe-editorial", type: "photo", category: "Photography" }
    ]
  },
  {
    slug: "axel-morin",
    name: "Axel Morin",
    categories: ["Commercials", "Music Videos"],
    tags: ["Film"],
    localVideo: "assets/tomake_bois.mp4",
    projects: [
      { client: "Prada", title: "Autumn Winter", slug: "prada-aw", type: "video", category: "Commercials" },
      { client: "Dior", title: "Fragrance", slug: "dior-fragrance", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "bleunuit",
    name: "Bleunuit",
    categories: ["Music Videos", "Fashion Films"],
    tags: ["Film"],
    localVideo: "assets/tomake_PIGMENTS.mp4",
    projects: [
      { client: "Rosalía", title: "Despechá", slug: "rosalia-despecha", type: "video", category: "Music Videos" },
      { client: "Christine and the Queens", title: "To Be Honest", slug: "catq-to-be-honest", type: "video", category: "Music Videos" }
    ]
  },
  {
    slug: "daniel-sannwald",
    name: "Daniel Sannwald",
    categories: ["Fashion Films", "Photography", "Music Videos"],
    tags: ["Film", "Photo"],
    localVideo: "assets/tomake_PIERRE.mp4",
    projects: [
      { client: "Alexander McQueen", title: "Campaign", slug: "mcqueen-campaign", type: "photo", category: "Photography" },
      { client: "Beyoncé", title: "Music Video", slug: "beyonce-mv", type: "video", category: "Music Videos" },
      { client: "Mugler", title: "Fashion Film", slug: "mugler-film", type: "video", category: "Fashion Films" }
    ]
  },
  {
    slug: "dorothea-sing-zhang",
    name: "Dorothea Sing Zhang",
    categories: ["Commercials", "Fashion Films"],
    tags: ["Film"],
    localVideo: "assets/tomake_bois.mp4",
    projects: [
      { client: "Hermès", title: "Spring Collection", slug: "hermes-spring", type: "video", category: "Fashion Films" },
      { client: "Louis Vuitton", title: "Campaign", slug: "lv-campaign", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "francois-rousselet",
    name: "François Rousselet",
    categories: ["Commercials", "Music Videos"],
    tags: ["Film"],
    previewVideo: "https://datamanagement.gosimian.com/assets/videos/FRO_Preview-MacBook-Pro-_Best-Performance-Yet.mp4",
    localVideo: "assets/tomake_PIERRE.mp4",
    projects: [
      { client: "MacBook Pro", title: "Best Performance Yet", slug: "macbook-pro-best-performance-yet", type: "video", category: "Commercials" },
      { client: "Coca-Cola × Star Wars", title: "The Collab", slug: "coca-cola-star-wars", type: "video", category: "Commercials" },
      { client: "NFL × Accenture", title: "The Pass", slug: "the-pass", type: "video", category: "Commercials" },
      { client: "Pharrell Williams ft. 21 Savage, Tyler, The Creator", title: "Cash In Cash Out", slug: "cash-in-cash-out", type: "video", category: "Music Videos" },
      { client: "Free Nationals, A$AP Rocky & Anderson .Paak", title: "Gangsta", slug: "gangsta", type: "video", category: "Music Videos" },
      { client: "Fila", title: "Campaign", slug: "fila-campaign", type: "video", category: "Commercials" },
      { client: "John Lewis", title: "Christmas", slug: "john-lewis-christmas", type: "video", category: "Commercials" },
      { client: "Diesel", title: "Francesca", slug: "diesel-francesca", type: "video", category: "Commercials" },
      { client: "Nike", title: "Nothing Beats a Londoner", slug: "nike-londoner", type: "video", category: "Commercials" },
      { client: "The Rolling Stones", title: "Angry", slug: "rolling-stones-angry", type: "video", category: "Music Videos" }
    ]
  },
  {
    slug: "gabriel-moses",
    name: "Gabriel Moses",
    categories: ["Commercials", "Music Videos"],
    tags: ["Film"],
    previewVideo: "https://datamanagement.gosimian.com/assets/videos/GMO_Preview-Corteiz-x-New-Era_Unreplaceable.mp4",
    localVideo: "assets/tomake_METAL.mp4",
    projects: [
      { client: "Corteiz × New Era", title: "Unreplaceable", slug: "corteiz-x-new-era-unreplaceable", type: "video", category: "Commercials" },
      { client: "Timberland", title: "Campaign", slug: "timberland", type: "video", category: "Commercials" },
      { client: "Clipse", title: "Chains and Whips", slug: "chains-and-whips", type: "video", category: "Music Videos" },
      { client: "Travis Scott", title: "Music Video", slug: "travis-scott", type: "video", category: "Music Videos" },
      { client: "The Last Hour", title: "Documentary", slug: "the-last-hour", type: "video", category: "Commercials" },
      { client: "Nike", title: "Unveil", slug: "nike-unveil", type: "video", category: "Commercials" },
      { client: "All Day I Dream About Sport", title: "Documentary", slug: "documentary", type: "video", category: "Commercials" },
      { client: "Adidas × Y-3", title: "Campaign", slug: "adidas-y3", type: "video", category: "Commercials" },
      { client: "Byredo", title: "Parfums", slug: "byredo-parfums", type: "video", category: "Commercials" },
      { client: "Little Simz", title: "No Thank You", slug: "little-simz-no-thank-you", type: "video", category: "Music Videos" }
    ]
  },
  {
    slug: "ilya-chemetoff",
    name: "Ilya Chemetoff",
    categories: ["Fashion Films", "Commercials"],
    tags: ["Film"],
    localVideo: "assets/tomake_TEXTILE.mp4",
    projects: [
      { client: "Jacquemus", title: "Le Chiquito", slug: "jacquemus-chiquito", type: "video", category: "Fashion Films" },
      { client: "Sézane", title: "Campaign", slug: "sezane-campaign", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "lola-raban",
    name: "Lola Raban",
    categories: ["Music Videos", "Fashion Films"],
    tags: ["Film"],
    localVideo: "assets/tomake_bois.mp4",
    projects: [
      { client: "Aya Nakamura", title: "Djadja", slug: "aya-djadja", type: "video", category: "Music Videos" },
      { client: "Coperni", title: "Show Film", slug: "coperni-show", type: "video", category: "Fashion Films" }
    ]
  },
  {
    slug: "marius-gonzalez",
    name: "Marius Gonzalez",
    categories: ["Commercials", "Music Videos"],
    tags: ["Film"],
    localVideo: "assets/tomake_PIERRE.mp4",
    projects: [
      { client: "New Balance", title: "Campaign", slug: "new-balance-campaign", type: "video", category: "Commercials" },
      { client: "Harry Styles", title: "As It Was", slug: "harry-styles-as-it-was", type: "video", category: "Music Videos" }
    ]
  },
  {
    slug: "massimiliano-bomba",
    name: "Massimiliano Bomba",
    categories: ["Commercials", "Fashion Films"],
    tags: ["Film"],
    localVideo: "assets/tomake_PIGMENTS.mp4",
    projects: [
      { client: "Fendi", title: "Campaign", slug: "fendi-campaign", type: "video", category: "Fashion Films" },
      { client: "Bulgari", title: "Jewellery", slug: "bulgari-jewellery", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "mati-diop",
    name: "Mati Diop",
    categories: ["Fashion Films", "Music Videos"],
    tags: ["Film"],
    localVideo: "assets/tomake_METAL.mp4",
    projects: [
      { client: "Maison Margiela", title: "Artisanal", slug: "margiela-artisanal", type: "video", category: "Fashion Films" },
      { client: "Childish Gambino", title: "This Is America", slug: "childish-gambino-america", type: "video", category: "Music Videos" }
    ]
  },
  {
    slug: "max-siedentopf",
    name: "Max Siedentopf",
    categories: ["Music Videos", "Commercials"],
    tags: ["Film"],
    localVideo: "assets/tomake_PIERRE.mp4",
    projects: [
      { client: "Tame Impala", title: "The Less I Know The Better", slug: "tame-impala", type: "video", category: "Music Videos" },
      { client: "Adidas Originals", title: "Original is Never Finished", slug: "adidas-originals", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "mrzyk-and-moriceau",
    name: "Mrzyk & Moriceau",
    categories: ["Music Videos", "Fashion Films"],
    tags: ["Film"],
    localVideo: "assets/tomake_bois.mp4",
    projects: [
      { client: "Dua Lipa", title: "Levitating", slug: "dua-lipa-levitating", type: "video", category: "Music Videos" },
      { client: "Kenzo", title: "World", slug: "kenzo-world", type: "video", category: "Fashion Films" }
    ]
  },
  {
    slug: "naghmeh-pour",
    name: "Naghmeh Pour",
    categories: ["Photography", "Fashion Films"],
    tags: ["Photo", "Film"],
    localVideo: "assets/tomake_TEXTILE.mp4",
    projects: [
      { client: "Vogue", title: "Editorial", slug: "vogue-editorial", type: "photo", category: "Photography" },
      { client: "Bottega Veneta", title: "Campaign", slug: "bottega-veneta", type: "photo", category: "Photography" }
    ]
  },
  {
    slug: "og-kids",
    name: "OG Kids",
    categories: ["Music Videos", "Commercials"],
    tags: ["Film"],
    localVideo: "assets/tomake_PIGMENTS.mp4",
    projects: [
      { client: "AWGE", title: "Project", slug: "awge-project", type: "video", category: "Music Videos" },
      { client: "Can-Am", title: "Campaign", slug: "can-am-campaign", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "sanjay-de-silva",
    name: "Sanjay De Silva",
    categories: ["Commercials", "Music Videos"],
    tags: ["Film"],
    localVideo: "assets/tomake_METAL.mp4",
    projects: [
      { client: "Bonnie Banane", title: "Music Video", slug: "bonnie-banane-mv", type: "video", category: "Music Videos" },
      { client: "Mugler", title: "Campaign", slug: "mugler-campaign", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "simon-cahn",
    name: "Simon Cahn",
    categories: ["Commercials", "Music Videos"],
    tags: ["Film"],
    localVideo: "assets/tomake_bois.mp4",
    projects: [
      { client: "Fontaines D.C.", title: "Music Video", slug: "fontaines-dc", type: "video", category: "Music Videos" },
      { client: "New York City Ballet", title: "Campaign", slug: "nycb-campaign", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "thibaut-grevet",
    name: "Thibaut Grevet",
    categories: ["Commercials", "Fashion Films", "Photography"],
    tags: ["Film", "Photo"],
    localVideo: "assets/tomake_PIERRE.mp4",
    projects: [
      { client: "Nike × Travis Scott", title: "Field Jaxx", slug: "field-jaxx", type: "photo", category: "Photography" },
      { client: "Hermès", title: "Spring Summer", slug: "hermes-ss", type: "video", category: "Fashion Films" },
      { client: "Adidas", title: "Campaign", slug: "adidas-campaign", type: "video", category: "Commercials" }
    ]
  },
  {
    slug: "torso",
    name: "Torso",
    categories: ["Music Videos", "Fashion Films"],
    tags: ["Film"],
    localVideo: "assets/tomake_TEXTILE.mp4",
    projects: [
      { client: "Disclosure", title: "Music Video", slug: "disclosure-mv", type: "video", category: "Music Videos" },
      { client: "Valentino", title: "Campaign", slug: "valentino-campaign", type: "video", category: "Fashion Films" }
    ]
  }
];

const HOMEPAGE = {
  featuredProject: {
    director: "Gabriel Moses",
    client: "Nike",
    previewVideo: "https://datamanagement.gosimian.com/assets/videos/GMO_Preview-Nike_Unveil.mp4",
    localVideo: "assets/tomake_METAL.mp4",
    slug: "nike-unveil",
    directorSlug: "gabriel-moses"
  },
  clientTicker: [
    "Nike", "Hermès", "MacBook Pro", "Maison Margiela", "Adidas Originals",
    "Harry Styles", "New Balance", "Mugler", "Bonnie Banane", "Coperni",
    "New York City Ballet", "Fontaines D.C.", "Coca-Cola × Star Wars",
    "AWGE", "Can-Am", "NFL × Accenture", "Travis Scott", "Dior",
    "Jacquemus", "Valentino", "Byredo", "Little Simz", "Kenzo", "Fila"
  ]
};

const AWARDS = [
  {
    festival: "D&AD",
    total: "108",
    unit: "pencils",
    highlight: "7 Black Pencils — Production Company of the Year 2014, 2016, 2021–2025",
    projects: [
      { title: "Nike — Air Jordan × Travis Scott", description: "Yellow Pencil in Sound Design & Use of Music · Wood Pencil in Cinematography for Fashion Film", slug: "air-jordan-x-travis-scott" },
      { title: "Pharrell Williams — Cash In Cash Out", description: "Yellow Pencil in Music Video Direction", slug: "cash-in-cash-out" },
      { title: "MacBook Pro — Best Performance Yet", description: "Wood Pencil in Direction for Commercials", slug: "macbook-pro-best-performance-yet" },
      { title: "Little Simz — No Thank You", description: "Graphite Pencil in Music Video", slug: "little-simz-no-thank-you" }
    ]
  },
  {
    festival: "CDA",
    total: "188",
    unit: "awards",
    highlight: "Most Awarded Production Company at French Art Directors Club 2025",
    projects: [
      { title: "Hermès — Spring Collection", description: "Or — Meilleure Direction Artistique", slug: "hermes-spring" },
      { title: "Jacquemus — Le Chiquito", description: "Argent — Film de Mode", slug: "jacquemus-chiquito" },
      { title: "Fontaines D.C. — Music Video", description: "Bronze — Clip Musical", slug: "fontaines-dc" }
    ]
  },
  {
    festival: "Cannes Lions",
    total: "27",
    unit: "lions",
    highlight: "8 Gold Lions",
    projects: [
      { title: "NFL × Accenture — The Pass", description: "Gold Lion — Film Craft", slug: "the-pass" },
      { title: "Coca-Cola × Star Wars", description: "Silver Lion — Film", slug: "coca-cola-star-wars" },
      { title: "Nike — Unveil", description: "Bronze Lion — Sport", slug: "nike-unveil" }
    ]
  },
  {
    festival: "UKMVA",
    total: "26",
    unit: "awards",
    highlight: "Production Company of the Year 2022",
    projects: [
      { title: "Little Simz — No Thank You", description: "Best R&B / Soul Video", slug: "little-simz-no-thank-you" },
      { title: "Rolling Stones — Angry", description: "Best Rock Video", slug: "rolling-stones-angry" }
    ]
  },
  {
    festival: "AICP",
    total: "5",
    unit: "awards",
    highlight: "Since 2022",
    projects: [
      { title: "MacBook Pro — Best Performance Yet", description: "Direction", slug: "macbook-pro-best-performance-yet" }
    ]
  },
  {
    festival: "CICLOPE",
    total: "24",
    unit: "awards",
    highlight: "2 Grand Prix (2022, 2023)",
    projects: [
      { title: "Pharrell Williams — Cash In Cash Out", description: "Grand Prix — Music Videos", slug: "cash-in-cash-out" },
      { title: "Little Simz — No Thank You", description: "Grand Prix — Music Videos", slug: "little-simz-no-thank-you" }
    ]
  },
  {
    festival: "MTV VMAs",
    total: "2",
    unit: "moonmen",
    highlight: "2 Moonmen",
    projects: [
      { title: "Corteiz × New Era — Unreplaceable", description: "Best Cinematography", slug: "corteiz-x-new-era-unreplaceable" }
    ]
  }
];

const CONTACT = {
  intro: "Paris-based Creative director, CGI generalist and VFX supervisor. Sometimes exploring photography, video and graphic design.",
  inquiries: [
    { label: "General Inquiries", email: "noemie.ducly@gmail.com" },
    { label: "Instagram", email: "@noemieducly" },
    { label: "Location", email: "Paris, France" }
  ],
  team: [
    {
      section: "Founders & Direction",
      members: [
        { role: "Founder | CEO", name: "Arno Moria" },
        { role: "Founder | MD / EP", name: "Jules de Chateleux" },
        { role: "VP | Fashion & Luxury", name: "Gwendoline Victoria" },
        { role: "MD / EP | America", name: "Jacq Wilkinson" },
        { role: "MD / EP | UK", name: "Elena Argiros" },
        { role: "MD / EP | APAC", name: "Genevieve Triquet" }
      ]
    },
    {
      section: "Production",
      members: [
        { role: "Executive Producers", name: "Andréa Dagourou, Charlotte Lepot, Evan Djenki, Hugo Marcel, Morgan Benson-Taylor, Mounia Mebarki, Smith, Théo Gall, Valentine Gomes-Ferenczi" },
        { role: "Head of Production", name: "Aurélie Bruneau" },
        { role: "Producers", name: "Alice Wills, Ernest Bouvier" },
        { role: "Line Producers", name: "Mateo Murga, Mathilde Hamart" },
        { role: "Photo Agent", name: "Lara Abdessalem" },
        { role: "Senior Project Manager", name: "Anne-Sophie Dujon" },
        { role: "Photo Producer", name: "Morgane Tayeau" }
      ]
    },
    {
      section: "Administration & Sales",
      members: [
        { role: "Office Managers", name: "Nathalie Catanzano, Rachel Ganachaud" },
        { role: "Sales — West Coast", name: "Steven Monkarsh, Irma Rodriguez" },
        { role: "Sales — East Coast", name: "Jonathan Jakubowicz, Alex Corn" }
      ]
    }
  ],
  offices: [
    { city: "Paris", address: "27, rue Michel Le Comte", postcode: "75003 Paris" }
  ],
  socials: [
    { label: "Instagram", url: "https://www.instagram.com/noemieducly/" },
    { label: "LinkedIn", url: "https://www.linkedin.com/in/noémie-ducly-505863205" }
  ],
  global: [
    { label: "Internships", email: "internships@division.global" },
    { label: "Contact Us", email: "hello@division.global" }
  ]
};

const REGIONS = [
  { code: "US", label: "US", url: "#", current: true },
  { code: "NL", label: "NL", url: "#" },
  { code: "APAC", label: "APAC", url: "#" },
  { code: "FR", label: "FR", url: "#" },
  { code: "UK", label: "UK", url: "#" }
];

function getDirector(slug) {
  return DIRECTORS.find(d => d.slug === slug) || null;
}

function getProject(slug) {
  for (const director of DIRECTORS) {
    const project = director.projects.find(p => p.slug === slug);
    if (project) return { director, project };
  }
  return null;
}
