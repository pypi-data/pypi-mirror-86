define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {

    var _renderPostfixCode = function(numpyPageRendererThis) {
        // var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-block', 'vp-user-option-box', 'vp-minimize' );
        sbTagString.appendLine("<div class='vp-accordion-header' >");
        sbTagString.appendFormatLine("<div class='{0} {1}' >", 'vp-panel-area-vertical-btn', 'vp-arrow-down');
        sbTagString.appendLine("</div>");
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'Postfix Code');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</div>");
        sbTagString.appendFormatLine("<div id='{0}'>", 'vp_postfixBox');
        sbTagString.appendFormatLine("<textarea class='{0} {1}' placeholder='{2}' rows='3' cols='60'>", 
                                                'vp-numpy-textarea', 'vp-numpy-postfix-textarea', 'postfix code');
        sbTagString.appendLine("</textarea>");
        sbTagString.appendLine("</div>");
        sbTagString.appendLine("</div>");

        var postfixDom = $(sbTagString.toString());  

        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
        mainPage.append(postfixDom);

        mainPage.on('focus', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        mainPage.on('blur', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.enable();
        });

        /** postfix Code */
        $(importPackageThis.wrapSelector(`.vp-numpy-postfix-textarea`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                postfixCode: $(this).val()
            });
        });
    }
    return _renderPostfixCode;
});