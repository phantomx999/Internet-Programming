function submitCell(cell_name, col) {
		name = document.getElementById("cell_name").value;
		color = document.getElementById("col").value;
		if (color == "bblue")
			document.getElementById(name).className = "blue1";
		else
			document.getElementById(name).className = "red1";
}

function resetBoard(){
		document.getElementById("one").className = "tictactoeText";
		document.getElementById("two").className = "tictactoeText";
		document.getElementById("three").className = "tictactoeText";
		document.getElementById("four").className = "tictactoeText";
		document.getElementById("five").className = "tictactoeText";
		document.getElementById("six").className = "tictactoeText";
		document.getElementById("seven").className = "tictactoeText";
		document.getElementById("eight").className = "tictactoeText";
		document.getElementById("nine").className = "tictactoeText";
}


