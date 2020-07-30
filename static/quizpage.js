
$( document ).ready(function() {
    $('textarea').autoResize();
});

function submitQuiz()
{
    var corr_answers = 0;
    var i;
    var input_answers = [];
    var tot_qs = document.getElementById("tot_qs").value;
    console.log(tot_qs);
    for (i=1; i<=tot_qs; i++ )
    {
        var id = 'ans_'+i.toString();
        var ans = document.getElementById(id).value;
        console.log(ans);
        input_answers.push(ans);
    }
    console.log(input_answers);

    document.getElementById("QuestionPaper").style.display = "none";
    document.getElementById("ReportCard").style.display = "inline";

    for(i=1; i<=tot_qs; i++)
    {
        var yourid='yourans_'+i.toString();
        var corrid = 'corrans_'+i.toString();
        var id = 'ans_'+i.toString();
        var statusid = 'status_'+i.toString();
        document.getElementById(yourid).value=document.getElementById(id).value;
        if(document.getElementById(yourid).value==document.getElementById(corrid).value)
        {
            corr_answers++;
        }
        else{
            document.getElementById(statusid).innerHTML="Status: Incorrect"
            document.getElementById(statusid).className="alert alert-danger"
        }

    }
    document.getElementById("total-correct").value=corr_answers;
    document.getElementById("total-questions").value = tot_qs;
}


/*
 * jQuery autoResize (textarea auto-resizer)
 * @copyright James Padolsey http://james.padolsey.com
 * @version 1.04
 */

(function($){
    
    $.fn.autoResize = function(options) {
        
        // Just some abstracted details,
        // to make plugin users happy:
        var settings = $.extend({
            onResize : function(){},
            animate : true,
            animateDuration : 150,
            animateCallback : function(){},
            extraSpace : 20,
            limit: 1000
        }, options);
        
        // Only textarea's auto-resize:
        this.filter('textarea').each(function(){
            
                // Get rid of scrollbars and disable WebKit resizing:
            var textarea = $(this).css({resize:'none','overflow-y':'hidden'}),
            
                // Cache original height, for use later:
                origHeight = textarea.height(),
                
                // Need clone of textarea, hidden off screen:
                clone = (function(){
                    
                    // Properties which may effect space taken up by chracters:
                    var props = ['height','width','lineHeight','textDecoration','letterSpacing'],
                        propOb = {};
                        
                    // Create object of styles to apply:
                    $.each(props, function(i, prop){
                        propOb[prop] = textarea.css(prop);
                    });
                    
                    // Clone the actual textarea removing unique properties
                    // and insert before original textarea:
                    return textarea.clone().removeAttr('id').removeAttr('name').css({
                        position: 'absolute',
                        top: 0,
                        left: -9999
                    }).css(propOb).attr('tabIndex','-1').insertBefore(textarea);
					
                })(),
                lastScrollTop = null,
                updateSize = function() {
					
                    // Prepare the clone:
                    clone.height(0).val($(this).val()).scrollTop(10000);
					
                    // Find the height of text:
                    var scrollTop = Math.max(clone.scrollTop(), origHeight) + settings.extraSpace,
                        toChange = $(this).add(clone);
						
                    // Don't do anything if scrollTip hasen't changed:
                    if (lastScrollTop === scrollTop) { return; }
                    lastScrollTop = scrollTop;
					
                    // Check for limit:
                    if ( scrollTop >= settings.limit ) {
                        $(this).css('overflow-y','');
                        return;
                    }
                    // Fire off callback:
                    settings.onResize.call(this);
					
                    // Either animate or directly apply height:
                    settings.animate && textarea.css('display') === 'block' ?
                        toChange.stop().animate({height:scrollTop}, settings.animateDuration, settings.animateCallback)
                        : toChange.height(scrollTop);
                };
            
            // Bind namespaced handlers to appropriate events:
            textarea
                .unbind('.dynSiz')
                .bind('keyup.dynSiz', updateSize)
                .bind('keydown.dynSiz', updateSize)
                .bind('change.dynSiz', updateSize);
            
        });
        
        // Chain:
        return this;
        
    };
    
    
    
})(jQuery);