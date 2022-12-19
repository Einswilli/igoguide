let docmap=document.querySelector('#map')
let detmap=document.querySelector('#detmap')

class GoogleMap{

    constructor(){
        let map=null
        let bounds=null
        let textMarker=null
    }
     async load(element){
        /* Charge la carte dans l'element passé en parametre AIzaSyCD7BvR3RtGHKwPXt_Q6vaSzvwTYzNIZ_0*/
        return new Promise((resolve,reject)=>{
            $script('https://maps.googleapis.com/maps/api/js?key=AIzaSyCD7BvR3RtGHKwPXt_Q6vaSzvwTYzNIZ_0',()=>{

                this.textMarker=class TextMarker extends google.maps.OverlayView {

                    constructor (pos, map, text) {
                        super()
                        this.div = null
                        this.html=null
                        this.pos = pos
                        this.text = text
                        this.setMap(map)
                        this.enablecallbacks=[]
                    }
                
                    onAdd () {
                        var x='';
                        this.div = document.createElement('div')
                        this.div.classList.add('marker')
                        this.div.style.position = 'absolute'
                        //alert(this.text)
                        this.div.innerHTML =this.text// "<img src=\""+this.text+"\">"
                        this.div.dataset.num=this.text
                        this.getPanes().overlayImage.appendChild(this.div)
                        this.div.addEventListener('click',()=>{
                            this.div.innerHTML=this.html
                            // this.isCurrent()
                            let currentItem=document.querySelector('.is-current')
                            if(currentItem!==null){
                                currentItem.classList.remove('is-current')
                                currentItem.innerHTML=currentItem.dataset.num
                            }
                            this.div.classList.add('is-current')
                            // this.div.style.width=170+'px'
                            this.div.style.padding='0px 0px 0px 0px'
                            // this.div.style.top = (this.div.style.top-this.div.style.height)+ "px"
                        })
                    }
                
                    draw () {
                        let position = this.getProjection().fromLatLngToDivPixel(this.pos)
                        this.div.style.left = position.x + "px"
                        this.div.style.top = position.y + "px"
                    }
                
                    onRemove () {
                        this.div.parentNode.removeChild(this.div)
                    }

                    activate(){
                        if (this.div!==null)this.div.classList.add('is-active')
                    }

                    deactivate(){
                        if (this.div!==null)this.div.classList.remove('is-active')
                    }

                    isCurrent(){
                        if (this.div!==null){
                            this.div.innerHTML=this.html
                            this.div.classList.add('is-current')
                        }
                        for(let cb of this.enablecallbacks){cb()}
                    }

                    passCurrent(){
                        if (this.div!==null){
                            this.div.innerHTML=this.text
                            this.div.classList.remove('is-current')
                        }
                    }

                    setContent(html){
                        this.html=html
                    }
                
                }

                // var center={lat:-25.363,lng:131.044}
                this.map=new google.maps.Map(element,{
                    zoom:8,
                    //gestureHandling: "cooperative"
                })
                this.bounds=new google.maps.LatLngBounds()
                google.maps.event.addListener(this.map,'zoom_changed',()=>{
                    //alert('zoom_changed')
                    let b=this.map.getBounds()
                    //alert(b)
                    // let items=document.querySelectorAll('.js-marker')
                    // for(let item of items){
                    //     alert(b)
                    // }
                })
                resolve()
            })
        })
    }

    addMarker(lat,lng,name){
        let coord=new google.maps.LatLng(lat,lng)
        let marker=new this.textMarker(
            coord,
            this.map,
            name
        )
        marker.enablecallbacks.push(()=>{
            this.map.setCenter(marker.pos)
        })
        // let marker=new google.maps.Marker({
        //     position:coord,
        //     map:this.map
        // })
        this.bounds.extend(coord)
        return marker
    }

    centerMap(){
        this.map.panToBounds(this.bounds)
        this.map.fitBounds(this.bounds)
    }
}
const initMap= async function(){
    let map=new GoogleMap()
    let activeMarker=null
    let currentMarker=null
    await map.load(docmap).then(function(){
        let items=document.querySelectorAll('.js-marker')
        for(let item of items){
            let marker=map.addMarker(item.dataset.lat,item.dataset.lng,item.dataset.num)
            marker.setContent(item.innerHTML)
            // marker.div.addEventListener('click',function(){
            //     marker.isCurrent()
            //     if(currentMarker!==null)currentMarker.passCurrent()
            //     currentMarker=marker
            // })
            item.addEventListener('mouseenter',function(){
                marker.activate()
                if(activeMarker!==null)activeMarker.deactivate()
                activeMarker=marker
            })

            item.addEventListener('mouseleave',function(){
                if(activeMarker===marker){
                    marker.deactivate()
                    activeMarker=null
                }
            })
        }
        map.centerMap()
    })
    return true
}
const detMap=async function(){
    let map=new GoogleMap()
    await map.load(detmap).then(function(){
        let item=document.querySelector('#detmap')
        //for(let item of items){
        map.addMarker(item.dataset.lat,item.dataset.lng,item.dataset.num)
        //}
        map.centerMap()
    })
    return true
}
if(docmap!==null){
    initMap()
}
if(detmap!==null){
    detMap()
}
