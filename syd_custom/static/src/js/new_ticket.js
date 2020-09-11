function hideSeverityLevels(e) { 

	if(isIssue(e)==true){
		setParamsForIssue(e); 
		
	} else if (isQuestion(e)==true){
		setParamsForQuestion(e); 
		
	} else { 
		setParamsForConfiguration(e); 
	}
}


function isIssue(e){
	return (e.selectedIndex=='2')
}

function isQuestion(e){
	return (e.selectedIndex=='1')
}

/* Issue */
function setParamsForIssue(e){
		// Environment, obbligatorio: Production/UAT/Development-Test (li vedo tutti)
		document.getElementById('select_environment').options[1].style.display = 'inline-block'; 
		document.getElementById('select_environment').options[2].style.display = 'inline-block';	
		document.getElementById('select_environment').options[2].style.display = 'inline-block';
		
		
		// Severity, obbligatorio: Comestic/Minor/Major/Critical
		document.getElementById('select_severity').options[0].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[1].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[2].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[3].style.display = 'inline-block'; 
		
}

function setParamsForQuestion(e){
		// Environment, Non obbligatorio: Production/UAT/Development-Test (li vedo tutti)
		document.getElementById('select_environment').options[1].style.display = 'inline-block'; 
		document.getElementById('select_environment').options[2].style.display = 'inline-block';	
		document.getElementById('select_environment').options[2].style.display = 'inline-block';
		
		// Severity, non obbligatorio: Cosmetic/Minor
		document.getElementById('select_severity').options[0].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[1].style.display = 'none'; 
		document.getElementById('select_severity').options[2].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[3].style.display = 'none'; 
}

function setParamsForConfiguration(e){
		// Environment, Non obbligatorio: Production/UAT/Development-Test
		document.getElementById('select_environment').options[1].style.display = 'inline-block'; 
		document.getElementById('select_environment').options[2].style.display = 'none';	
		document.getElementById('select_environment').options[3].style.display = 'inline-block';
		
		// Severity, non obbligatorio: Cosmetic/Minor
		document.getElementById('select_severity').options[0].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[1].style.display = 'none'; 
		document.getElementById('select_severity').options[2].style.display = 'inline-block'; 
		document.getElementById('select_severity').options[3].style.display = 'none'; 
}

