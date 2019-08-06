function setupText(hoverItem){
        hp = document.getElementById("popupword");
        hp.style.display="none";
		
 	hp = document.getElementById("popupsearch");
	if (hp)        hp.style.display="none";
  	hp = document.getElementById("popuplist");
   	if(hp)     hp.style.display="none";
 	
}
function writeWord(){
hp = document.getElementById("popupword");
      hp.style.display="visible";
        hp.style.display="block";
        hp.style.float="left";
}
function writeList(){
  hp = document.getElementById("popuplist");
  hp.style.display="block";
}
function writeSearch(){
  hp = document.getElementById("popupsearch");
  hp.style.display="block";
  hp.style.float="left";

}

function stopText(el){
hp = document.getElementById(el);
hp.style.display="none";
}
function DHTMLText(text){
 
 hp=document.getElementById("popupword");
     if(hp){
     	hp.style.display="block";
	hp.style.width="15%";
     }
  if (navigator.appName == "Microsoft Internet Explorer")

        hp.innerHTML=text+' <a onclick="stopText()"> <div style="float:right;"><a onclick=stopText("popupword") >Close</a><\div>';
  else if (navigator.appName != "Netscape")

        hp.innerHTML=text+' <div style="float:right;"><a onclick=stopText("popupword")  >Close</a><\div>';
  else

        hp.innerHTML=text+' <div style="float:right;"><a onclick=stopText("popupword")   >Close</a><\div> ';



}

function  DHTMLSoundnoTextFull(surl){

	DHTMLSound(surl,"");


}
function DHTMLSound(surl, text) {

   hp=document.getElementById("popupword");
     if(hp) {
	    hp.style.display="none";
		hp.style.width="35%";
	}
	files=surl.split(';')
	
        text =files[0]+' <audio controls="None" autoplay> <source height="30px" src="' + files[1]+ '"    type="audio/mpeg"></audio>'
	//ignore first and last ';'?
        for (i=2; i<files.length-1;i++){
	   console.log("first")
	   console.log(files[i])
           console.log(files[i+1])
	   text +='<br>'+files[i]+'<audio controls="None" > <source height="30px" src="' + files[i+1]+ '"    type="audio/mpeg"></audio>'
	   // more than one item so need controller
	   hp.style.display="block";
	   i+=1; //adding a comment as to source of each file ( as first file reference) so skip two each entry
	}
	hp.innerHTML=text+' '+'<div style="float:right;"><a onclick=stopText("popupword")  >Close</a><\div> ';
}

function stopText(){
hp=document.getElementById("popupword");
         hp.innerHTML="";
	hp.style.display="none";
	hp.style.width="0%";
}
function DHTMLFrontSound(surl,text) {
   hp=document.getElementById("popupword");
     if(hp) {
            hp.style.display="block";
	 hp.style.background="grey";
                hp.style.width="100%";
        }
   surl="/sounds/"+surl;

        hp.innerHTML=text+' '+'<audio controls autoplay> <source height="30px" src="' + surl+ '"    type="audio/mpeg"></audio><div style="float:right;"><a onclick=stopText("popupword")  ></a><\div> ';

}
function DHTMLVideo(vurl){
 hp=document.getElementById("popupword");

 hp.innerHTML='<object height="344"><param name="movie" value="'+vurl+'"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="'+vurl+'" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" height="344"></embed></object>';
  
 hp.style.display="block";
}
