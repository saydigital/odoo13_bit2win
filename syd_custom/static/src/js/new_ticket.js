function body_onLoad(e){
}


function formValidate(e){

}

function hideSeverityLevels(e) { 
	if(e.selectedIndex=='1'){
		document.getElementById('select_severity').options[1].style.display = 'none'; 
		document.getElementById('select_severity').options[2].style.display = 'none'; 
		
		severity_selected = document.getElementById('select_severity').selectedIndex
		if(severity_selected == '1' || severity_selected == '2'){
			document.getElementById('select_severity').selectedIndex = 0
		}
	
	} else {
		document.getElementById('select_severity').options[1].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[2].style.display = 'inline-block'; 
	}
}