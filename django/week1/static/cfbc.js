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

function addPlayer( pos, name, id ) {
   console.log( "Position: " + pos + " Name: " + name + " Id: " + id )
   // Add to pick-table
   var picks = document.getElementById( "pick-table" ).getElementsByTagName( "tr" )
   var dropping = false
   for( var i = 0; i < picks.length; i++ ) {
      var row = picks[ i ]
      if( row.cells[ 0 ].innerText.toLowerCase() == pos 
          && row.cells[ 1 ].innerText == name ) {
         dropping = true
         break
      }
   }
   var otherId = -1
   for( var i = 0; i < picks.length; i++ ) {
      var row = picks[ i ]
      if( row.cells[ 0 ].innerText.toLowerCase() == pos ) {
         if( row.cells[ 1 ].innerText == name ) {
            row.cells[ 1 ].innerHTML = "None"
            break
         } else if( row.cells[ 1 ].innerText == "None" && !dropping ) {
            row.cells[ 1 ].innerHTML = name 
            row.cells[ 1 ].setAttribute( 'espnId', id )
            break
         } else {
            otherId = row.cells[ 1 ].getAttribute( 'espnId' )
         }
      }
   }
   
   // change icons
   var statsTable = document.getElementById( id )
   var button = statsTable.children[ 0 ].getElementsByTagName( "i" )[ 0 ]
   if( dropping ) {
      button.setAttribute( "class", "fa fa-plus" )
   } else {
      button.setAttribute( "class", "fa fa-minus" )
   }
   if( otherId != -1 && pos != 'td' && pos != 'tk' ) {
      // change all icons except the set players to locked
      var statsRows = document.getElementsByClassName( "stats-row" )
      for( var i = 0; i < statsRows.length; i++ ) {
         var button = stastRows[ i ].getElementsByTagName( "i" )[ 0 ]
         button.setAttribute( "class", "fa fa-lock" )
      }
   }
}

window.onload = function() {
   showTable( 'qb' )
}
