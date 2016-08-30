function sortByField( playerTable, direction, sort ) {
   console.log( "sortByField( " + playerTable + ", " + direction + ", " + sort + " )" )
   if( sort == null ) {
      console.log( "no sort specified" )
      return 
   }
   // bubble sort the rows, using the sort function
   var tbody = playerTable.getElementsByTagName( "tbody" )[ 0 ]
   var rows = tbody.getElementsByTagName( "tr" )
   // [ 0  |  1  |  2  | ...  |  length - 1 ]
   //   i     j
   for( var i = 0; i < rows.length; i++ ) {
      var sorted = true
      for( var j = 0; j < rows.length - 1; j++ ) {
         var sort_result = sort( rows[ j ], rows[ j + 1 ] )
         if( ( sort_result > 0 && direction == "down" ) || ( sort_result < 0 && direction == "up" ) ) {
            var tmp = rows[ j + 1 ]
            tbody.removeChild( rows[ j + 1 ] )
            tbody.insertBefore( tmp, rows[ j ] )
            sorted = false
         } // else if 0, no change is necessary
      }
      if( sorted ) {
         break
      }
   }
}

function fieldSorter( headerCol ) {
   var playerTable = getPlayerTable( headerCol )
   var sort = null
   var direction = 'up'

   // Change html class so we know this is sorted
   // Also change the chevrons for that visual sex appeal
   // (yes, I used sex appeal in a comment because I fucking wanted to)
   if( headerCol.getAttribute( 'sort_direction' ) == 'up' ) {
      direction = 'down'
   }
   var headers = headerCol.parentElement.cells
   var headerIdx = -1
   for( var i = 0; i < headers.length; i++ ) {
      var icon = headers[ i ].getElementsByTagName( 'i' )[ 0 ]
      if( headers[ i ] == headerCol ) {
         headerIdx = i
         headers[ i ].setAttribute( 'sort_direction', direction )
         if( icon ) {
            icon.className = "fa fa-chevron-" + direction 
         } else {
            headers[ i ].innerHTML += "    <i class=\"fa fa-chevron-" + direction + "\" aria-hidden=\"true\"></i>"
         }
      } else {
         if( icon ) {
            icon.parentElement.removeChild( icon )
         }
         headers[ i ].removeAttribute( 'sort_direction' )
      }
   }

   // use the id of the header to select the correct sorting function 
   // sorting functions take two rows and return 1 if the first is "larger"
   // 0 if they are "equal" and -1 if the first is "smaller"
   if( headerCol.id == "sort-pick" ) {
      sort = sortSelected 
   } else if( headerCol.id == "sort-player" ) {
      sort = sortPlayer
   } else if( headerCol.id == "sort-opp" ) {
      sort = sortStraightByIdx( headerIdx, -1 )
   } else if( headerCol.id == "sort-ca" ) {
      sort = sortCompAttempts( headerIdx )
   } else {
      sort = sortNumByIdx( headerIdx )
   }

   sortByField( playerTable, direction, sort )
}

function sortCompAttempts( idx ) {
   return function sortCompAttempts( l, r ) {
      var transform = function( text ) {
         var splat = text.split( "/" )       
         var numerator = parseInt( splat[ 0 ] )
         var denominator = parseInt( splat[ 1 ] )
         if( denominator == 0 ) {
            return 0
         }
         return numerator / denominator
      }
      var l_percentage = transform( l.cells[ idx ].innerHTML )
      var r_percentage = transform( r.cells[ idx ].innerHTML )
      return straightSort( l_percentage, r_percentage )
   }
}

function sortNumByIdx( idx, invert=1 ) {
   return function( l, r ) {
      return invert * straightSort( parseInt( l.cells[ idx ].innerHTML ), parseInt( r.cells[ idx ].innerHTML ) )
   }
}

function sortStraightByIdx( idx, invert=1 ) {
   return function( l, r ) {
      return invert * straightSort( l.cells[ idx ].innerHTML, r.cells[ idx ].innerHTML )
   }
}

function sortPlayer( l, r ) {
   var l_name = l.getElementsByClassName( "name-field" )[ 0 ].innerText
   var r_name = r.getElementsByClassName( "name-field" )[ 0 ].innerText
   return -1 * straightSort( l_name, r_name )
}

function straightSort( l, r ) {
   if( l > r ) {
      return 1
   } else if( l == r ) {
      return 0
   } else {
      return -1
   }
}

function sortSelected( l, r ) {
   var iconToInt = function( icon ) {
      var cls = icon.className
      if( cls.includes( 'minus' ) ) {
         return 1
      } else {
         return 0 
      }
   }
   // get icon
   var l_icon = l.getElementsByTagName( "i" )[ 0 ]
   var r_icon = r.getElementsByTagName( "i" )[ 0 ]
   return iconToInt( l_icon ) - iconToInt( r_icon )
}

function getPlayerTable( e ) {
   var elem = e
   var positions = [ 'qb', 'rb', 'wr', 'td', 'pk' ]
   while( elem ) {
      if ( positions.indexOf( elem.id ) != -1 && elem.nodeName == "TABLE" ) {
         return elem
      }
      elem = elem.parentElement 
   }
}

function showTable( table ) {
   var tables = document.getElementsByClassName( "pure-table player-list" )
   for( var i = 0; i < tables.length; i++ ) {
      if( tables[ i ].id == table ) {
	 tables[ i ].style.display = 'inline-block'
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

function dropPlayer( pos, name, id, team ) {
   console.log( "dropPlayer Position: " + pos + " Name: " + name + " Id: " + id + " Team: " + team)
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
      var cur_team = rows[ i ].getAttribute( 'team' )
      var button = rows[ i ].getElementsByTagName( "button" )[ 0 ]
      var icon = rows[ i ].getElementsByTagName( "i" )[ 0 ]
      var cur_name = rows[ i ].children[ 1 ].innerText.trim()
      console.log( "cur_team: " + cur_team )
      if( cur_id != otherId ) {
         //change to plus
         button.setAttribute( "class", "pure-button" )
         button.setAttribute( "onClick", "addPlayer( \"" + pos + "\",\"" + cur_name + "\", " + cur_id + ",\"" + cur_team + "\")" )
         icon.setAttribute( "class", "fa fa-plus" )
      }
      if( cur_id == id ) {
         rows[ i ].removeAttribute( 'class' )
      }
   }
}

function addPlayer( pos, name, id, team ) {
   console.log( "addPlayer Position: " + pos + " Name: " + name + " Id: " + id + " Team: " + team )
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
            row.cells[ 1 ].innerHTML = "<div class=pure-g><div class=pure-u-4-24><img class=small-icon src=/static/" + team + ".png/></div>" + "<div class=pure-u-20-24><p>" + name  + "</p></div>"
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
      var cur_team = rows[ i ].getAttribute( 'team' )
      if( cur_id == id ) {
         // change it to the minus
         button.setAttribute( "class", "pure-button" )
         button.setAttribute( "onClick", "dropPlayer( \"" + pos + "\",\"" + name + "\"," + id + ",\"" + cur_team + "\")" )
         icon.setAttribute( "class", "fa fa-minus" )
         rows[ i ].setAttribute( "class", 'cfbc-picked' )
      } else if( ( otherId != null && otherId != cur_id ) || pos == 'pk' || pos == 'td' ) {
         //change to lock
         button.setAttribute( "class", "pure-button pure-button-disabled" )
         button.removeAttribute( "onClick" )
         icon.setAttribute( "class", "fa fa-lock" )
      }
   }
}

function hideAlert(){ 
   window.location.hash = ''
}

//window.onload = function() {
//   showTable( 'qb' )
//}
