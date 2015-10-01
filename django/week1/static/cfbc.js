function showTable( table ) {
   tables = document.getElementsByClassName( "pure-table player-list" )
   for( var i = 0; i < tables.length; i++ ) {
      if( tables[ i ].id == table ) {
	 tables[ i ].style.display = 'block'
      } else {
	 tables[ i ].style.display = 'none'
      }
   }
}

function selectMenuTab( tab ) {
   selected = document.getElementsByClassName( "pure-menu-item pure-menu-selected" )[ 0 ]
   if( selected ) {
      selected.className = "pure-menu-item"
   }
   tab.className = "pure-menu-item pure-menu-selected"
}

function selectPos( tab, table ) {
   selectMenuTab( tab )
   showTable( table )
}

function addPlayer( pos, name ) {
   console.log( "Position: " + pos + " Name: " + name )
}

window.onload = function() {
   showTable( 'qb' )
}
