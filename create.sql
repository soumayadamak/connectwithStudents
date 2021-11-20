use sdammak_db ;
drop table if exists hasHobby;
drop table if exists fromCountry;
drop table if exists inClub;
drop table if exists hasMajor;
drop table if exists student;
drop table if exists hobby;
drop table if exists country;
drop table if exists club;
drop table if exists major;
 
create table country(
   cid int auto_increment not null  primary key,
   name varchar(20)
)
ENGINE = innoDB;

create table club (
   clid int auto_increment not null primary key,
   clubName varchar(20)
)
ENGINE = innoDB;

create table major(
   mid int auto_increment not null primary key,
   majorName varchar(20)
)
Engine = innoDB;
 
create table student(
   nm int auto_increment not null  primary key ,
   name varchar(20) not null,
   email varchar(20) not null,
   unique(email),
   index(email),
   password char(60) not null,
   profile varchar(1024),
   mentor  varchar(3),
   mentee bit,
   class SET("2022","2023","2024","2025") not null,
   race SET("Native American/Alaska Native", "Black/African American", "White/non Hispanic","Asian","Middle Eastern/North African","Hispanic/Latinx","Pacific Islander","Not Listed"),
   firstGen set("First Generation", "Low Income Background"),
   spritiual set("Christianity","Islam","Judaism","Hinduism","Buddhism","Sikhism","Traditional African Religions","Native American Religion","Paganism","Unitarian Universalism","Spiritual","Daoism"),
   personality set("INTJ", "INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"),
   immigration set("International Student", "Refugee","My Family immigrated to the US", "US citizen but lived abroad","Dual Citizen of the US and another country"),
   city set("Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"),
   bio varchar(250) not null,
   career set("Architecture", "Engineering","Arts", "Entertainment","Business", "Finance", "Consulting","Communications","Community and social services","Education","Science and technology","Government", "Non-profit","Health and medicine"," Law and public policy","Sales")       
)
 
ENGINE = innoDB;
create table hobby(
   hb int auto_increment not null  primary key,
   name varchar(20)
)
ENGINE = innoDB;
 
create table hasHobby(
   nm int ,
   hb int ,
   foreign key (nm) references student(nm)
       on update cascade
       on delete restrict ,
   foreign key (hb) references hobby(hb)
       on update cascade
       on delete restrict
)
ENGINE = innoDB;
 
create table fromCountry(
   nm int ,
   cid int ,
   foreign key (nm) references student(nm)
       on update cascade
       on delete restrict ,
   foreign key (cid) references country(cid)
       on update cascade
       on delete restrict
)
ENGINE = innoDB;
 
create table hasMajor(
   nm int ,
   mid int ,
   foreign key (nm) references student(nm)
       on update cascade
       on delete restrict ,
   foreign key (mid) references major(mid)
       on update cascade
       on delete restrict
)
ENGINE = innoDB;
 
create table inClub(
   nm int ,
   clid int ,
   foreign key (nm) references student(nm)
       on update cascade
       on delete restrict ,
   foreign key (clid) references club(clid)
       on update cascade
       on delete restrict
)
ENGINE = innoDB;

Insert into club(clubName) values ("Biology and Biochemistry Club"), ("Chinese Classical Arts ClubAcademic Organization"), ("Club RocksAcademic Organization"), ("Economic Student Association (ESA)\tAcademic Organization"), ("Greco-Roman SocietyAcademic Organization"), ("Neuroscience Club"), ("Psychology Club"), ("Quiz Bowl"), ("Society of Physics Students"), ("Student Interdisciplinary Data Initiative (SIDI)"), ("A.S.T.R.O"), ("Chinese Classical Arts Club"), ("180 Degrees Consulting"), ("Hippocratic Society"), ("Investment Society"), ("Minority Association of Premedical Students (MAPS)"), ("Pre-Dental Society (PDS)"), ("Wellesley College Pre-Law Society"), ("Wellesley Consulting Club"), ("Wellesley For Asset Management and Finance (WAMF)"), ("Wellesley in Business"), ("Wellesley in Service and Leadership"), ("2022 Class Council"), ("2023 Class Council"), ("2024 Class Council"), ("2025 Class Council"), ("Appointed Representatives Committee"), ("College Government"), ("College Government President's Council"), ("Committee for Political Engagement"), ("Committee on Organization Recognition Affairs (CORA)"), ("Club Water PoloClub Sport"), ("Wellesley College Archery Club"), ("Wellesley College Club Sailing"), ("Wellesley College Club Squash"), ("Wellesley College Rugby Football Club"), ("Wellesley College Ultimate Frisbee (Whiptails)"), ("Wellesley Equestrian Team"), ("Wellesley Nordic Ski Club (Nordic Ski)"), ("Bangladeshi Students Association"), ("blackOUT"), ("Chinese Students' Association (CSA)"), ("Cielito Lindo (CL)"), ("Club Filipina"), ("Ethos"), ("Fusion"), ("German Club"), ("Hui O Hawaii"), ("Italian Society - La Società Italiana"), ("Balance Health Educators (BHEs)"), ("Blue Cancer Society (BCS)"), ("Sexual Assault Awareness for Everyone (SAAFE)"), ("Munger Hall HC"), ("Pomeroy Hall HC"), ("Severance Hall HC"), ("Chrysalis Zine"), ("Counterpoint"), ("Film Society"), ("GenerAsians"), ("Kaleidoscope"), ("Legenda"), ("The Wellesley GlobalistMedia"), ("The Wellesley News"), ("The Wellesley Review (TWR)"), ("W.Collective"), ("Civic Engagement"), ("Club Sports"), ("Inclusion and Engagement"), ("Ministrare Counci"), ("Office of Intercultural Education"), ("PLTC"), ("Recreation"), ("Residential Life and Housing"), ("AscenDance"), ("Brandeis-Wellesley Orchestra (BWO)"), ("Sexual Health Educators (SHEs)"), ("Wellesley Students vs Pandemics (WSvP)"), ("Bates Hall HC"), ("Beebe Hall HC"), ("Cazenove Hall HC"), ("HCHouse Council"), ("Claflin Hall HC"), ("Freeman Hall HC"), ("House Presidents' Council"), ("McAfee Hall HC"), ("Chamber Music Society (CMS)"), ("Dead Serious Improv"), ("Guild of Carillonneurs"), ("MIT Wellesley Toons"), ("The Fiddleheads"), ("The Wellesley College Blue Notes"), ("The Wellesley Widows"), ("Wellesley Aiko"), ("Awaken The Dawn"), ("Wellesley College Democrats (WC Dems)"), ("Wellesley College Republicans"), ("BOW Climbing Club"), ("BOW Figure Skating Club (BOW FSC)"), ("Wellesley College Ballroom Dance Team (WBDT)"), ("Wellesley College ITF Taekwon-Do Club"), ("Wellesley College Shotokan Karate Club"), ("Wellesley Futsal Club"), ("Wellesley Quidditch"), ("Al-Muslimat (ALM)"), ("Asian Baptist Student Koinonia (ABSK)"), ("Black Women's Ministry (BWM)"), ("BOW Climbing Club"), ("BOW Figure Skating Club (BOW FSC)"), ("Cru Wellesley Christian Fellowship (Cru)"), ("Darshana"), ("Heartspace Unitarian Universalist"), ("InterVarsity Christian Fellowshi"), ("Latter-day Saint Student Association"), ("Newman Catholic Ministry"), ("Symphony Church"), ("Advocates for North Korean Human Rights (ANKHR)"), ("EnAct"), ("Humanize"), ("One for the World"), ("Period@Wellesley"), ("She's the First at Wellesley College (STF)"), ("Students for an Accessible Wellesley (SAW)"), ("Wellesley Against Mass Incarceration (WAMI)"), ("Wellesley Asian Alliance (WAA)"), ("Wellesley College Girl Up"), ("Active Minds at Wellesley"), ("Agora Society"), ("Alpha Kappa Chi History Society (AKX)"), ("Alpha Phi Sigma Lecture Society (Phi Sig)"), ("Shakespeare SocietySociety"), ("Society Zeta Alpha (ZA)"), ("Tau Zeta Epsilon Society (TZE)"), ("Audio Engineering Society"), ("Botanistas"), ("Chess Club"), ("Familia"), ("Fine Art Society"), ("Mock Trial"), ("Model UN"), ("Phocus Photography Club (Phocus)"), ("Prism Think Tank (Prism)"), ("Quiz Bowl"), ("Office of Student Involvement"), ("Office of Student Wellness"), ("ORSL"), ("Girls Group"), ("Girls Who Code"), ("Global Medical Brigades"), ("Habitat for Humanity"), ("Hear Your Song Wellesley (HYS Wellesley)"), ("Robogals"), ("Science Learning and Mentoring (SLAM)"), ("Wellesley College Special Olympics Club"), ("Wellesley for Boston Children's Hospital");

Insert into country(name) values ("Afghanistan"), ("Aland Islands"), ("Albania"), ("Algeria"), ("American Samoa"), ("Andorra"), ("Angola"), ("Anguilla"), ("Antarctica"), ("Antigua and Barbuda"), ("Argentina"), ("Armenia"), ("Aruba"), ("Australia"), ("Austria"), ("Azerbaijan"), ("Bahamas"), ("Bahrain"), ("Bangladesh"), ("Barbados"), ("Belarus"), ("Belgium"), ("Belize"), ("Benin"), ("Bermuda"), ("Bhutan"), ("Bolivia"), ("Bonaire/Saint Eustatius and Saba "), ("Bosnia and Herzegovina"), ("Botswana"), ("Brazil"), ("British Indian Ocean Territory"), ("British Virgin Islands"), ("Brunei"), ("Bulgaria"), ("Burkina Faso"), ("Burundi"), ("Cambodia"), ("Cameroon"), ("Canada"), ("Cape Verde"), ("Cayman Islands"), ("Central African Republic"), ("Chad"), ("Chile"), ("China"), ("Christmas Island"), ("Cocos Islands"), ("Colombia"), ("Comoros"), ("Cook Islands"), ("Costa Rica"), ("Croatia"), ("Cuba"), ("Curacao"), ("Cyprus"), ("Czech Republic"), ("Democratic Republic of the Congo"), ("Denmark"), ("Djibouti"), ("Dominica"), ("Dominican Republic"), ("East Timor"), ("Ecuador"), ("Egypt"), ("El Salvador"), ("Equatorial Guinea"), ("Eritrea"), ("Estonia"), ("Ethiopia"), ("Falkland Islands"), ("Faroe Islands"), ("Fiji"), ("Finland"), ("France"), ("French Guiana"), ("French Polynesia"), ("French Southern Territories"), ("Gabon"), ("Gambia"), ("Georgia"), ("Germany"), ("Ghana"), ("Gibraltar"), ("Greece"), ("Greenland"), ("Grenada"), ("Guadeloupe"), ("Guam"), ("Guatemala"), ("Guernsey"), ("Guinea"), ("Guinea-Bissau"), ("Guyana"), ("Haiti"), ("Honduras"), ("Hong Kong"), ("Hungary"), ("Iceland"), ("India"), ("Indonesia"), ("Iran"), ("Iraq"), ("Ireland"), ("Isle of Man"), ("Israel"), ("Italy"), ("Ivory Coast"), ("Jamaica"), ("Japan"), ("Jersey"), ("Jordan"), ("Kazakhstan"), ("Kenya"), ("Kiribati"), ("Kuwait"), ("Kyrgyzstan"), ("Laos"), ("Latvia"), ("Lebanon"), ("Lesotho"), ("Liberia"), ("Libya"), ("Liechtenstein"), ("Lithuania"), ("Luxembourg"), ("Macao"), ("Macedonia"), ("Madagascar"), ("Malawi"), ("Malaysia"), ("Maldives"), ("Mali"), ("Malta"), ("Marshall Islands"), ("Martinique"), ("Mauritania"), ("Mauritius"), ("Mayotte"), ("Mexico"), ("Micronesia"), ("Moldova"), ("Monaco"), ("Mongolia"), ("Montenegro"), ("Montserrat"), ("Morocco"), ("Mozambique"), ("Myanmar"), ("Namibia"), ("Nauru"), ("Nepal"), ("Netherlands"), ("New Caledonia"), ("New Zealand"), ("Nicaragua"), ("Niger"), ("Nigeria"), ("Niue"), ("Norfolk Island"), ("North Korea"), ("Northern Mariana Islands"), ("Norway"), ("Oman"), ("Pakistan"), ("Palau"), ("Palestine"), ("Panama"), ("Papua New Guinea"), ("Paraguay"), ("Peru"), ("Philippines"), ("Pitcairn"), ("Poland"), ("Portugal"), ("Puerto Rico"), ("Qatar"), ("Republic of the Congo"), ("Reunion"), ("Romania"), ("Russia"), ("Rwanda"), ("Saint Barthelemy"), ("Saint Helena"), ("Saint Kitts and Nevis"), ("Saint Lucia"), ("Saint Martin"), ("Saint Pierre and Miquelon"), ("Saint Vincent and the Grenadines"), ("Samoa"), ("San Marino"), ("Sao Tome and Principe"), ("Saudi Arabia"), ("Senegal"), ("Serbia"), ("Seychelles"), ("Sierra Leone"), ("Singapore"), ("Sint Maarten"), ("Slovakia"), ("Slovenia"), ("Solomon Islands"), ("Somalia"), ("South Africa"), ("South Georgia and the South Sandwich Islands"), ("South Korea"), ("South Sudan"), ("Spain"), ("Sri Lanka"), ("Sudan"), ("Suriname"), ("Svalbard and Jan Mayen"), ("Swaziland"), ("Sweden"), ("Switzerland"), ("Syria"), ("Taiwan"), ("Tajikistan"), ("Tanzania"), ("Thailand"), ("Togo"), ("Tokelau"), ("Tonga"), ("Trinidad and Tobago"), ("Tunisia"), ("Turkey"), ("Turkmenistan"), ("Turks and Caicos Islands"), ("Tuvalu"), ("U.S. Virgin Islands"), ("Uganda"), ("Ukraine"), ("United Arab Emirates"), ("United Kingdom"), ("United States"), ("United States Minor Outlying Islands"), ("Uruguay"), ("Uzbekistan"), ("Vanuatu"), ("Vatican"), ("Venezuela"), ("Vietnam"), ("Wallis and Futuna"), ("Western Sahara"), ("Yemen"), ("Zambia"), ("Zimbabwe"), ("Myanmar");

Insert into major(majorName) values ("Africana Studies"), ("American Studies"), ("Anthropology"), ("Studio Art"), ("Astronomy"), ("Biological Sciences"), ("Chemistry"), ("Classical Studies"), ("Cognitive & Linguistic Science"), ("Computer Science"), ("East Asian Languages and Cultures"), ("Economics"), ("Education"), ("English"), ("Environmental Studies"), ("French"), ("Geosciences"), ("German Studies"), ("History "), ("Italian Studies"), ("Linguistics"), ("Mathematics"), ("Music"), ("Neuroscience"), ("Philosophy"), ("Physics"), ("Political Science"), ("Psychology"), ("Religion"), ("Russian"), ("Sociology"), ("Spanish"), ("Women’s and Gender Studies"), ("Asian American Studies"), ("Architecture"), ("Astrophysics"), ("Biochemistry"), ("Chemical Physics"), ("Cinema and Media Studies"), ("Cognitive and Linguistic Sciences"), ("Comparative Literary Studies"), ("Comparative Race and Ethnicity"), ("East Asian Studies"), ("French Cultural Studies"), ("International Relations"), ("Jewish Studies"), ("Latin American Studies"), ("Media Arts and Sciences"), ("Medieval/Renaissance Studies"), ("Middle Eastern Studies"), ("Peace and Justice Studies"), ("Russian Area Studies"), ("South Asia Studies"), ("Theatre Studies"), ("Arabic"), ("Chinese"), ("Greek"), ("Hebrew"), ("Hindi/Urdu"), ("Japanese"), ("Korean"), ("Latin"), ("Portuguese"), ("Swahili"), ("Data Science");