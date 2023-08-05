define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {
    /**
     * numpy의 dtype을 선택하는 <div> 블록을 생성하는 렌더링 함수
     * numpy의 모든 함수에서 dtype을 입력받는 state 이름은 dtype이다
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderDtypeBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
        var numpyDtypeArray = numpyPageRendererThis.numpyDtypeArray;

        var sbTagString = new sb.StringBuilder();

        sbTagString.appendFormatLine("<div class='{0} {1} {2}' ", 'vp-numpy-option-block', 'vp-spread', 'vp-numpy-style-flex-row' );
        sbTagString.appendFormatLine("     style='{0}' >", 'padding-top: 10px' );
        sbTagString.appendFormatLine("<table style='{0}' >", 'width: 100%' );
        sbTagString.appendLine("<tr>" );
        sbTagString.appendLine("<td style='width: 40%;'>" );
        sbTagString.appendLine("<label class='vp-multilang' data-caption-id='selectDtype'>" );
        sbTagString.appendFormatLine("{0}", 'Select Dtype');
        sbTagString.appendLine("</label>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("<td>" );
        sbTagString.appendFormatLine("<select class='vp-numpy-select-dtype' id='{0}'>", `vp_numpyDtype-${uuid}` );
        sbTagString.appendLine("</select>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("</tr>" );
        sbTagString.appendLine("</table>" );
        sbTagString.appendLine("</div>" );
        
        var dtypeBlock = $(sbTagString.toString());
   
        // var dtypeBlock = $(`<div class='vp-numpy-option-block vp-spread vp-numpy-style-flex-row' id='vp_blockArea'
        //                          style='padding-top: 10px;'>
        //                         <table style='width: 100%;'>
        //                             <tr>
        //                                 <td style='width: 40%;'>
        //                                     <label for='i0' class='vp-multilang' data-caption-id='selectDtype'
        //                                            style='margin-bottom: 0px;'> 
        //                                         Select Dtype
        //                                     </label>
        //                                 </td>
                                        
        //                                 <td>
        //                                     <select class='vp-numpy-select-dtype' id='vp_numpyDtype-${uuid}'>
        //                                     </select>
        //                                 </td>
        //                             </tr>
        //                         </table>
        //                     </div>`);
                       
        optionPage.append(dtypeBlock);

        /** src/common/const_numpy.js에서 설정한 dtype 배열 값을 <select>태그 안에 
         * <option>태그 value안에 동적 렌더링 
         */
        numpyDtypeArray.forEach(function (element) {
            $(importPackageThis.wrapSelector(`#vp_numpyDtype-${uuid}`)).append(`<option value='${element.value}'> ${element.name}</option>`)
        });

        /** dtype 선택  이벤트 함수 */
        $(importPackageThis.wrapSelector(`#vp_numpyDtype-${uuid}`)).change(function()  {
            numpyStateGenerator.setState({
                dtype: $(':selected', this).val()
            });
        });
    }
    return _renderDtypeBlock;
});
