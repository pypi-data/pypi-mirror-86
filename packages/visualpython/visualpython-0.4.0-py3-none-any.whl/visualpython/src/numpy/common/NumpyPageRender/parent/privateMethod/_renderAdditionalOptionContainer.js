define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {

    var _renderAdditionalOptionContainer = function(numpyPageRendererThis) {
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
     
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-optionPageBlock-view', 'vp-numpy-block', 'vp-minimize' );
        sbTagString.appendFormatLine("<div class='{0}'>", 'vp-accordion-header');
        sbTagString.appendFormatLine("<div class='{0} {1}' >", 'vp-panel-area-vertical-btn', 'vp-arrow-down');
        sbTagString.appendLine("</div>");
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'Additional Options');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</div>");
        sbTagString.appendLine("</div>");

        var additionalOptionDom = $(sbTagString.toString());  
        optionPage.append(additionalOptionDom);

    }
    return _renderAdditionalOptionContainer;
});