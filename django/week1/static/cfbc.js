function showTable( t ) {
   tables = document.getElementsByClassName( "pure-table player-list" )
   for( var i = 0; i < tables.length; i++ ) {
      if( tables[ i ].id == t ) {
	 tables[ i ].style.display = 'block'
      } else {
	 tables[ i ].style.display = 'none'
      }
   }
}

window.onload = function() {
   showTable( 'qb' )
}
