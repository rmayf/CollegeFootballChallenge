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

function dropPlayer( pos, name, id ) {
   console.log( "dropPlayer Position: " + pos + " Name: " + name + " Id: " + id )
   // Remove from picks-window
   var picks = document.getElementById( "pick-table" ).getElementsByTagName( "tr" )
   for( var i = 0; i < picks.length; i++ ) {
      var row = picks[ i ]
      if( row.cells[ 0 ].innerText.toLowerCase() == pos ) {
         if( row.cells[ 1 ].innerText == name ) {
            row.cells[ 1 ].innerText = "None"
            row.cells[ 1 ].removeAttribute( 'espnId' ) 
            break
         }
      }
   }
   // Remove from hidden input
   // Also grab an otherId if exists
   otherId = null
   var inputs = document.getElementById( "pick-table" ).getElementsByTagName( "input" )
   for( var i = 0; i < inputs.length; i++ ) {
      if( inputs[ i ].getAttribute( 'position' ) == pos ) {
         if( inputs[ i ].getAttribute( 'value' ) == id ) {
            inputs[ i ].removeAttribute( 'value' )
         } else {
            otherId = inputs[ i ].getAttribute( 'value' )
         }
      }
   }
   // Change icons
   var playerTable = document.getElementById( pos ).getElementsByTagName( "tbody" )[ 0 ]
   var rows = playerTable.getElementsByTagName( "tr" )
   for( var i = 0; i < rows.length; i++ ) {
      var cur_id = rows[ i ].getAttribute( 'id' )
      var button = rows[ i ].getElementsByTagName( "button" )[ 0 ]
      var icon = rows[ i ].getElementsByTagName( "i" )[ 0 ]
      var cur_name = rows[ i ].children[ 1 ].innerText.trim()
      if( cur_id != otherId ) {
         //change to plus
         button.setAttribute( "class", "pure-button" )
         button.setAttribute( "onClick", "addPlayer( \"" + pos + "\",\"" + cur_name + "\", " + cur_id + ")" )
         icon.setAttribute( "class", "fa fa-plus" )
      }
      if( cur_id == id ) {
         rows[ i ].removeAttribute( 'class' )
      }
   }
}

function addPlayer( pos, name, id ) {
   console.log( "addPlayer Position: " + pos + " Name: " + name + " Id: " + id )
   // Add to pick-table
   var picks = document.getElementById( "pick-table" ).getElementsByTagName( "tr" )
   var otherId = null
   var set = false
   for( var i = 0; i < picks.length; i++ ) {
      var row = picks[ i ]
      if( row.cells[ 0 ].innerText.toLowerCase() == pos ) {
         if( row.cells[ 1 ].innerText == name ) {
            console.log( "Player already in picks table: " + name )
            return -1
         } else if( !set && row.cells[ 1 ].innerText == "None" ) {
            row.cells[ 1 ].innerHTML = name 
            row.cells[ 1 ].setAttribute( 'espnId', id )
            set = true
         } else {
            otherId = row.cells[ 1 ].getAttribute( 'espnId' )
         }
      }
   }

   // Add to hidden input field
   var inputs = document.getElementById( "pick-table" ).getElementsByTagName( "input" )
   for( var i = 0; i < inputs.length; i++ ) {
      if( inputs[ i ].getAttribute( 'position' ) == pos && inputs[ i ].getAttribute( 'value' ) == null ) {
         inputs[ i ].setAttribute( 'value', id )
         break
      }
   }

   // Change icons
   var playerTable = document.getElementById( pos ).getElementsByTagName( "tbody" )[ 0 ]
   var rows = playerTable.getElementsByTagName( "tr" )
   for( var i = 0; i < rows.length; i++ ) {
      var cur_id = rows[ i ].getAttribute( 'id' )
      var button = rows[ i ].getElementsByTagName( "button" )[ 0 ]
      var icon = rows[ i ].getElementsByTagName( "i" )[ 0 ]
      if( cur_id == id ) {
         // change it to the minus
         button.setAttribute( "class", "pure-button" )
         button.setAttribute( "onClick", "dropPlayer( \"" + pos + "\",\"" + name + "\"," + id + ")" )
         icon.setAttribute( "class", "fa fa-minus" )
         rows[ i ].setAttribute( "class", 'cfbc-picked' )
      } else if( ( otherId != null && otherId != cur_id ) || pos == 'tk' || pos == 'td' ) {
         //change to lock
         button.setAttribute( "class", "pure-button pure-button-disabled" )
         button.removeAttribute( "onClick" )
         icon.setAttribute( "class", "fa fa-lock" )
      }
   }
}

window.onload = function() {
   showTable( 'qb' )
}
