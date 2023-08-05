define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {

    /** CALL(호출) 변수를 입력하는 <div> 블럭 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderCallVarBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1}' id='{2}' style='padding-top: 10px;'>", 
                                           'vp-numpy-option-block', 'vp-spread', 'vp_blockArea');
        sbTagString.appendLine("<table style='width: 100%;'>" );        
        sbTagString.appendLine("<tr>" );
        sbTagString.appendLine("<td style='width: 40%;'>" );
        sbTagString.appendFormatLine("<label class='{0}' data-caption-id='{1}' style='margin-bottom: 0px;'> ",
                                            'vp-multilang', 'inputReturnVariable');
        sbTagString.appendFormatLine("{0}", '* Input Call Variable');
        sbTagString.appendLine("</label>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("<td>" );
        sbTagString.appendFormatLine("<input type='text' class='{0} {1}' id='{2}' placeholder='{3}'/>", 
                                            'vp-numpy-input', 'vp-numpy-callVar-input', `vp_numpyCallVarInput-${uuid}`, 'input variable');
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("</tr>" );
        sbTagString.appendLine("</table>" );
        sbTagString.appendLine("</div>" );
        
        var callVarBlock = $(sbTagString.toString()); 
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();

        var requiredTagSelector = numpyPageRendererThis.getRequiredPageSelector();
        var requiredPage = $(importPackageThis.wrapSelector(requiredTagSelector));
        requiredPage.append(callVarBlock);

        /** call 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyCallVarInput-${uuid}`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                callVariable: $(this).val()
            });
        });
    }

    return _renderCallVarBlock;
});