define([
    './constData.js'
], function ( constData ) {

    // const { deleteOneArrayValueAndGet } = api;
    const { BLOCK_CODELINE_TYPE
            , IMPORT_BLOCK_TYPE
            , FOCUSED_PAGE_TYPE

            , STR_NULL
            , STR_DIV
            , STR_SELECTED
            , STR_ONE_SPACE
            , STR_ONE_INDENT

            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS

            , STR_INPUT_YOUR_CODE
            , STR_ICON_ARROW_UP
            , STR_ICON_ARROW_DOWN
            , STR_BORDER 

            , STR_COLON_SELECTED
            , STR_CHANGE_KEYUP_PASTE

            , VP_CLASS_NODEEDITOR_LEFT
            , VP_CLASS_NODEEDITOR_RIGHT
            , VP_CLASS_NODEEDITOR_OPTION_TAB
            , VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED
            
            , STATE_classInParamList
            , STATE_className
            , STATE_defName
            , STATE_defInParamList
            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_ifConditionList

            , STATE_elifCodeLine
            , STATE_elifList
            , STATE_forCodeLine
            , STATE_whileCodeLine
            , STATE_breakCodeLine
            , STATE_passCodeLine
            , STATE_continueCodeLine
            , STATE_baseImportList
            , STATE_customImportList
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_isFinally
            , STATE_returnOutParamList
            , STATE_customCodeLine
            , STATE_propertyCodeLine

            , COLOR_GRAY_input_your_code
            , COLOR_FOCUSED_PAGE } = constData;

    var renderMainDom = function(that) {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block');
        mainDom.classList.add(`vp-block-${that.getUUID()}`);
        return mainDom;
    }
    var renderLeftHolderDom = function() {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block-left-holder');
        return mainDom;
    }
    var renderMainInnerDom = function() {
        var mainInnerDom = $(`<div class='vp-block-inner'></div>`);
        return mainInnerDom;
    }

    /** class param 생성 */
    var generateClassInParamList = function(that) {
        var classInParamList = that.getState(STATE_classInParamList);
        var classInParamStr = `(`;
        classInParamList.forEach(( classInParam, index ) => {
            if (classInParam !== '' ) {
                classInParamStr += `${classInParam}`;
                for (var i = index + 1; i < classInParamList.length; i++) {
                    if (classInParamList[i] !== '') {
                        classInParamStr += `, `;
                        break;
                    }
                };
            }
        });
        classInParamStr += `) : `;
        return classInParamStr;
    }

    /** def param 생성 */
    var generateDefInParamList = function(that) {
        /** 함수 파라미터 */
        var defInParamList = that.getState(STATE_defInParamList);
             
        var defInParamStr = `(`;
        defInParamList.forEach(( defInParam, index ) => {
            // console.log('defInParam', defInParam);

            const { defParamName, defDefaultVal ,defType } = defInParam;
            if (defParamName !== '' ) {
               
                defInParamStr += `${defParamName}`;
                if (defDefaultVal !== '') {
                    defInParamStr += ` = ${defDefaultVal}`;
                }

                for (var i = index + 1; i < defInParamList.length; i++) {
                    if (defInParamList[i].defParamName !== '') {
                        defInParamStr += `, `;
                        break;
                    }
                };
            }
        });
        defInParamStr += `) : `;
        return defInParamStr;
    }

    /** return param 생성 */
    var generateReturnOutParamList = function(that) {
        var returnOutParamList = that.getState(STATE_returnOutParamList);
        var returnOutParamStr = ` `;
        returnOutParamList.forEach(( returnInParam, index ) => {
            if (returnInParam !== '' ) {
                returnOutParamStr += `${returnInParam}`;
                for (var i = index + 1; i < returnOutParamList.length; i++) {
                    if (returnOutParamList[i] !== '') {
                        returnOutParamStr += `, `;
                        break;
                    }
                };
            }
        });
        returnOutParamStr += ``;
        return returnOutParamStr;
    }

    var generateIfConditionList = function(that) {
        var ifConditionList = that.getState(STATE_ifConditionList);
        var ifConditionListStr = ` `;
        ifConditionList.forEach(( ifCondition, index ) => {
            const { arg1, arg2, arg3, arg6 } = ifCondition;
            ifConditionListStr += `(`;
            ifConditionListStr += arg1;
            ifConditionListStr += ' ';
            ifConditionListStr += arg2;
            ifConditionListStr += ' ';
            ifConditionListStr += arg3;
            ifConditionListStr += ' ';
            ifConditionListStr += `)`;
            ifConditionListStr += ' ';

            if ( ifConditionList.length -1 !== index ) {
                ifConditionListStr += arg6;
            }

            ifConditionListStr += ' ';
        });

        return ifConditionListStr;
    }

    var renderMainHeaderDom = function(that) {
        /** class 이름 */
        var className = that.getState(STATE_className);
        /** class 파라미터 */
        var classInParamList = that.getState(STATE_classInParamList);
        var classInParamStr = generateClassInParamList(that);

        /** def 이름 */
        var defName = that.getState(STATE_defName);
        /** def 파라미터 */
        var defInParamList = that.getState(STATE_defInParamList);
        var defInParamStr = generateDefInParamList(that);

        /** return 파라미터*/
        var returnOutParamList = that.getState(STATE_returnOutParamList);
        var returnOutParamStr = generateReturnOutParamList(that);

        /** if */ 
        // var returnOutParamList = that.getState(STATE_returnOutParamList);
        var ifConditionStr = generateIfConditionList(that);

        var blockCodeType =  that.getBlockCodeLineType();
        var blockName = that.getBlockName();
        var isBreakOrContinueOrPassOrCode = false;
        if (blockCodeType === BLOCK_CODELINE_TYPE.BREAK || blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE 
            || blockCodeType === BLOCK_CODELINE_TYPE.PASS || blockCodeType === BLOCK_CODELINE_TYPE.PASS_SUB
            || blockCodeType === BLOCK_CODELINE_TYPE.CODE || blockCodeType === BLOCK_CODELINE_TYPE.PROPERTY) {
            isBreakOrContinueOrPassOrCode = true;
        }
        var blockUUID = that.getUUID();
        var mainHeaderDom = $(`<div class='vp-block-header'>
                                ${
                                    isBreakOrContinueOrPassOrCode === true    
                                        ? STR_NULL
                                        :  `<strong class='vp-nodeeditor-style-flex-column-center 
                                                ${that.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER 
                                                                                ? 'vp-block-name' 
                                                                                : ''}' 
                                                style='margin-right:30px; 
                                                       font-size:12px; 
                                                       color:#252525;'>
                                            ${blockName}
                                            </strong>`
                                }
                                <div class='vp-nodeeditor-codeline-ellipsis 
                                            vp-nodeeditor-codeline-container-box'>
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.CLASS   
                                                ? `<div class='vp-nodeeditor-style-flex-row'>
                                                        <div class='vp-block-header-class-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className}
                                                        </div>
                                                        <div class='vp-block-header-param
                                                                    vp-block-header-param-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className.length === 0 
                                                                ? ''
                                                                : classInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }

                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.DEF  
                                                ? `<div class='vp-nodeeditor-style-flex-row'>
                                                        <div class='vp-block-header-def-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${defName}
                                                        </div>
                                                        <div class='vp-block-header-param
                                                                    vp-block-header-param-${blockUUID}'
                                                                style='font-size:12px;'>
                                                                ${defName.length === 0 
                                                                    ? ''
                                                                    : defInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }
                                            

                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.IF    
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-if-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${ifConditionStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.FOR   
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-for-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_forCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.WHILE 
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-while-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_whileCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }   
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.ELIF
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-elif-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_elifCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-except-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_exceptCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.BREAK  
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-break-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_breakCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE  
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-continue-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_continueCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.PASS || blockCodeType === BLOCK_CODELINE_TYPE.PASS_SUB     
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-pass-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_passCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.CODE      
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-custom-code-${blockUUID}'
                                                        style='font-size:12px; color:${that.getState(STATE_customCodeLine) === STR_NULL 
                                                            ? `${COLOR_GRAY_input_your_code}` : ''};'>
                                                        ${that.getState(STATE_customCodeLine) === STR_NULL
                                                            ? STR_INPUT_YOUR_CODE
                                                            : that.getState(STATE_customCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.PROPERTY   
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-property-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_propertyCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.RETURN 
                                            || blockCodeType === BLOCK_CODELINE_TYPE.RETURN_SUB        
                                                ? `<div class='vp-block-header-param
                                                               vp-block-header-param-${blockUUID}'
                                                            style='font-size:12px;'>
                                                        ${returnOutParamStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                            
                                        </div>
                                </div>`);
        return mainHeaderDom;
    }

    var renderBottomOptionContainer = function() {
        return $(`<div class='vp-nodeeditor-style-flex-row-center' 
                       style='padding: 0.5rem;'></div>`);
    }

    var renderBottomOptionContainerInner = function() {
        return $(`<div class='vp-nodeeditor-blockoption 
                            vp-nodeeditor-option'
                       style='width: 95%;'>
                  </div>`);
    }

    var renderDomContainer = function() {
        var domContainer = $(`<div class='vp-nodeeditor-option-container'>
                                        <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                            <span class='vp-block-optiontab-name'>code</span>
                                            <div class='vp-nodeeditor-style-flex-row-center'>
                                                <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                            </div>
                                        </div>
                                    </div>`);
        return domContainer;
    }

    var renderBottomOptionInnerDom = function() {
        var innerDom = $(`<div class='vp-nodeeditor-option-container'>
                                    <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    
                                    </div>
                                </div>`);
                                // <span class='vp-block-optiontab-name'>name</span>
                                // <div class='vp-nodeeditor-style-flex-row-center'>
                                //     <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                // </div>
        return innerDom;
    }

    var renderIfConditionDom = function(that, blockCodeType) {
   
        var ifConditionListState = that.getState(STATE_ifConditionList);
        var uuid = that.getUUID();
        var classStr = `vp-nodeeditor-if-input-${uuid}`;
        var conditionContainer = $(`<div class='vp-block-blockoption 
                                          vp-nodeeditor-blockoption-block 
                                          vp-nodeeditor-blockoption-inner 
                                          vp-nodeeditor-style-flex-row-between' 
                                        style='position:relative;'>
                                               
                                </div>`);

        var columnDom = $(`<div class='vp-nodeeditor-style-flex-column-center'
                                style='width: 100%;'></div>`);
    
        var ifConditionListState = that.getState(STATE_ifConditionList);  
        ifConditionListState.forEach( (condition, index) => {

            /** arg6 isDisabled 체크 */
            var isDisabled = false;
            if ( ifConditionListState.length -1 === index ) {
                isDisabled = true;
            }

            const { arg1, arg2, arg3, arg6 } = condition;
                        
       
            var conditionDom = $(`<div class='vp-nodeeditor-style-flex-row-between
                                            ${classStr}'
                                        style=' margin-left: 28px; 
                                                ${index !== 0 ? 'margin-top: 5px;' : ''}'>
                                
                                        <span class='vp-nodeeditor-style-flex-column-center'
                                              style='margin-left: 5px; color: rgba(0,0,0,0.3);'> ${index + 1} </span>
                                        <span class='vp-nodeeditor-style-flex-column-center'
                                              style='margin-left: 5px;'> ( </span>
                                        <input class='vp-nodeeditor-blockoption-input
                                                      vp-nodeeditor-blockoption-if-arg
                                                      vp-nodeeditor-blockoption-if-arg1-${index}-${uuid}'
                                                value="${arg1}"
                                                placeholder='input arg'>
                                                                
                                        </input>
                                        <select class='vp-nodeeditor-select
                                                       vp-nodeeditor-blockoption-if-arg2-${index}-${uuid}'>
                                            <option value='==' ${arg2 === '==' ? STR_SELECTED : ''}>
                                                ==
                                            </option>
                                            <option value='!=' ${arg2 === '!=' ? STR_SELECTED : ''}>
                                                !=
                                            </option>
                                            <option value='>' ${arg2 === '>' ? STR_SELECTED : ''}>
                                                >
                                            </option>
                                            <option value='>' ${arg2 === '>' ? STR_SELECTED : ''}>
                                                <
                                            </option>
                                            <option value='>=' ${arg2 === '>=' ? STR_SELECTED : ''}>
                                                >= 
                                            </option>
                                            <option value='<=' ${arg2 === '<=' ? STR_SELECTED : ''}>
                                                <=
                                            </option>
                                        </select>  

                                        <input class='vp-nodeeditor-blockoption-input
                                                      vp-nodeeditor-blockoption-if-arg
                                                      vp-nodeeditor-blockoption-if-arg3-${index}-${uuid}'
                                                value="${arg3}"
                                                placeholder='input arg'>

                                        </input>
                                        <span class='vp-nodeeditor-style-flex-column-center'> ) </span>
                                        ${isDisabled === false 
                                            ? `<select class='vp-nodeeditor-select
                                                            vp-nodeeditor-blockoption-if-arg
                                                            vp-nodeeditor-blockoption-if-arg6-${index}-${uuid}'
                                                        style='width: 50%; min-width:52px;'>
                                                    
                                                    <option value='and' ${arg6 === 'and' ? STR_SELECTED : ''}>
                                                        and
                                                    </option>
                                                    <option value='or' ${arg6 === 'or' ? STR_SELECTED : ''}>
                                                        or
                                                    </option>

                                                </select>`   
                                            : `<div class='vp-nodeeditor-blockoption-if-arg'
                                                    style='border: transparent; width: 50%; min-width:52px;'>
                                                </div>`}
                                      
                                    
                                </div>`);  

            var plusConditionButton = $(`<button class='vp-nodeeditor-if-condition-plus-button 
                                                        vp-nodeeditor-if-condition-plus-button-${index}-${uuid} 
                                                        vp-block-btn'
                                                 style='margin-right:5px;'>
                                                        + 
                                        </button>`);

            var deleteConditionButton = $(`<button class='vp-nodeeditor-if-condition-delete-button 
                                                          vp-nodeeditor-if-condition-delete-button-${index}-${uuid} 
                                                          vp-block-btn'>
                                                        - 
                                           </button>`);  
            conditionDom.append(plusConditionButton);
            conditionDom.append(deleteConditionButton);
          
            columnDom.append(conditionDom);                 
        });
        conditionContainer.append(columnDom);     

                      
        // var deleteButton = $(`<button class='vp-nodeeditor-option-reset-button 
        //                                             vp-block-btn'>
        //                                 x
        //                             </button>`);
        // conditionDom.append(deleteButton);
        // conditionContainer.append(plusConditionButton);
        // conditionContainer.append(deleteConditionButton);
     
        return conditionContainer;
    }

    var renderBottomOptionName = function(that, name, blockCodeType, uuid) {
        var classStr = STR_NULL;
        var inputStyleStr = STR_NULL;
        var resetButton = null;
        var dropDownButton = null;
        var blockCodeName = that.getBlockName();
        var blockContainerThis = that.getBlockContainerThis();
        var uuid = that.getUUID();

        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-input-class-name-${uuid}`;
            blockCodeName = 'Name';
            inputStyleStr = 'width: 82%';
            /** state className에 문자열이 1개도 없을 때 */
            var classNameState = that.getState(STATE_className);
            if (classNameState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.DEF) {
            classStr = `vp-nodeeditor-input-def-name-${uuid}`;
            blockCodeName = 'Name';
            inputStyleStr = 'width: 82%';
            /** state defName에 문자열이 1개도 없을 때 */
            var defNameState = that.getState(STATE_defName);
            if (defNameState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.IF) {
            classStr = `vp-nodeeditor-if-input-${uuid}`;
            inputStyleStr = 'width:90%;';
            /** state ifCodeLine에 문자열이 1개도 없을 때 */
            // var ifCodeLineState = that.getState(STATE_ifCodeLine);
            // if (ifCodeLineState === STR_NULL) {
            //     classStr += STR_ONE_SPACE;
            //     classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            // }

        } else if (blockCodeType === BLOCK_CODELINE_TYPE.FOR) {
            classStr = `vp-nodeeditor-for-input-${uuid}`;
            inputStyleStr = 'width:85%;';
            /** state forCodeLine에 문자열이 1개도 없을 때 */
            var forCodeLineState = that.getState(STATE_forCodeLine);
            if (forCodeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.WHILE) {
            classStr = `vp-nodeeditor-while-input-${uuid}`;
            inputStyleStr = 'width:80%;';
            /** state whileCodeLine에 문자열이 1개도 없을 때 */
            var whileCodeLineState = that.getState(STATE_whileCodeLine);
            if (whileCodeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.CODE) {
            classStr = `vp-nodeeditor-code-input-${uuid}`;

            /** state codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_customCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {

                that.setState({
                    customCodeLine: STR_NULL
                });
                $(`.vp-nodeeditor-code-input-${uuid}`).html(STR_NULL);
                $(`.vp-block-header-custom-code-${that.getUUID()}`).html(STR_INPUT_YOUR_CODE);
                $(`.vp-block-header-custom-code-${that.getUUID()}`).css('color','#d4d4d4');
                blockContainerThis.renderBlockOptionTab();
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.BREAK) {
            classStr = `vp-nodeeditor-break-input-${uuid}`;

            /** state break codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_breakCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    breakCodeLine: STR_BREAK
                });
                $(`.vp-nodeeditor-break-input-${uuid}`).text(STR_NULL);
                $(`.vp-block-header-break-${that.getUUID()}`).html(that.getState(STATE_breakCodeLine));
                blockContainerThis.renderBlockOptionTab();
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE) {
            classStr = `vp-nodeeditor-continue-input-${uuid}`;

            /** state continue codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_continueCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    continueCodeLine: STR_CONTINUE
                });
                $(`.vp-nodeeditor-continue-input-${uuid}`).text(STR_NULL);
                $(`.vp-block-header-continue-${that.getUUID()}`).html(that.getState(STATE_continueCodeLine));
                blockContainerThis.renderBlockOptionTab();
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.PASS || blockCodeType === BLOCK_CODELINE_TYPE.PASS_SUB) {
            classStr = `vp-nodeeditor-pass-input-${uuid}`;

            /** state pass codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_passCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    passCodeLine: STR_PASS
                });
                $(`.vp-nodeeditor-pass-input-${uuid}`).text(STR_NULL);
                $(`.vp-block-header-pass-${that.getUUID()}`).html(that.getState(STATE_passCodeLine));
                blockContainerThis.renderBlockOptionTab();
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.PROPERTY) {
            classStr = `vp-nodeeditor-property-input-${uuid}`;

            /** state property codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_propertyCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    propertyCodeLine: '@property'
                });
                $(`.vp-nodeeditor-property-input-${uuid}`).text(STR_NULL);
                $(`.vp-block-header-property-${that.getUUID()}`).html(that.getState(STATE_propertyCodeLine));
                blockContainerThis.renderBlockOptionTab();
            });
        }
        else if (blockCodeType === BLOCK_CODELINE_TYPE.ELIF) {
            classStr = `vp-nodeeditor-elif-input-${uuid}`;
        }
        else if (blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT) {
            classStr = `vp-nodeeditor-except-input-${uuid}`;
        }
        
        var nameDom = $(`<div class='vp-block-blockoption 
                                     vp-nodeeditor-blockoption-block 
                                     vp-nodeeditor-blockoption-inner 
                                     vp-nodeeditor-style-flex-row-between' 
                                style='position:relative;'>
                            ${
                                blockCodeType === BLOCK_CODELINE_TYPE.IF || blockCodeType === BLOCK_CODELINE_TYPE.FOR
                                || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.DEF
                                || blockCodeType === BLOCK_CODELINE_TYPE.CLASS
                                    ?  `<span class='vp-block-optiontab-name 
                                                     vp-nodeeditor-style-flex-column-center'>${blockCodeName}</span>`
                                    : ''
                               
                            }
                            <input class='vp-nodeeditor-blockoption-input ${classStr}'
                                   style='${inputStyleStr}' 
                                   value="${name}"
                                   placeholder='input code line' ></input>   
                                                                             
                        </div>`);
                        
        if (resetButton !== null) {
            $(nameDom).append(resetButton);
        }
        return nameDom;
    }

    var renderInParamContainer = function(block, inParamList) {
        var paramPlusStr = `vp-nodeeditor-param-plus-btn-${block.getUUID()}`;
        var paramDeleteStr = `vp-nodeeditor-param-delete-btn-${block.getUUID()}`;
        // <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
        var inParamContainer = $(`<div class='vp-nodeeditor-ifoption-container'>
                                            <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>
                                                    param</span>
                                                <div class='vp-nodeeditor-style-flex-row-center' >
                                                    <span class='vp-nodeeditor-number 
                                                                 vp-nodeeditor-style-flex-column-center'
                                                        style='margin-right:5px;'>
                                                        ${inParamList.length} Param
                                                    </span>
                                                    <button class='vp-block-btn ${paramPlusStr}'
                                                            style='margin-right:5px;'>
                                                        + 
                                                    </button>
                                                    <button class='vp-block-btn ${paramDeleteStr}'
                                                            style=''>
                                                        - 
                                                    </button>
                                          
                                                </div>
                                            </div>
                                        </div>`);
        return inParamContainer;
    }
    
    /** 인자 순서 조절 */
    var renderDefParamDom = function(block, defInParams, index) {
        const { defParamName, defDefaultVal ,defType } = defInParams;


        var uuid = block.getUUID();
        var classStr = `vp-nodeeditor-input-def-param-${index}-${uuid}`;
        var defaultCssClassStr = `vp-nodeeditor-input-defaultval-${index}-${uuid}`;
        var inParamDom = $(`<div class='vp-nodeeditor-style-flex-row'
                                style='margin-top:5px;'>

                                <div class='vp-nodeeditor-style-flex-column-center'
                                     style='margin:0 0.5rem; color: rgba(0,0,0,0.3);'>
                                    ${index+1}
                                </div>

                                <div class='vp-nodeeditor-blockoption-block
                                            vp-nodeeditor-blockoption-inner 
                                            vp-nodeeditor-style-flex-row' 
                                        style='position:relative; 
                                               margin-top:0px; 
                                               border:transparent;'>

                                    <input placeholder='input param' 
                                            class='vp-nodeeditor-blockoption-input 
                                                   vp-nodeeditor-blockoption-def-arg
                                                   ${classStr}' 
                                            style='width: 70%; '
                                          
                                            value='${defParamName}'>   

                                    <input placeholder='input value' 
                                            class='vp-nodeeditor-blockoption-input 
                                                   vp-nodeeditor-blockoption-def-arg
                                                   ${defaultCssClassStr}' 
                                            style='width: 70%; 
                                                   border: 1px solid #d4d4d4;'
                                            value='${defDefaultVal}'>  

                                    <select class='vp-nodeeditor-select
                                                   vp-nodeeditor-blockoption-def-arg
                                                   vp-nodeeditor-blockoption-def-type-select-${index}-${uuid}'>
                                        <option value='None' ${defType === 'None' ? STR_SELECTED : ''}>
                                            None
                                        </option>
                                        <option value='*args' ${defType === '*args' ? STR_SELECTED : ''}>
                                            *args
                                        </option>
                                        <option value='**kwargs' ${defType === '**kwargs' ? STR_SELECTED : ''}>
                                            **kwargs
                                        </option>
                                    </select>    

                                </div>
                            </div>`);
                  
        return inParamDom;
    }
    /** 인자 순서 조절 */
    var renderInParamDom = function(inParam, index, blockCodeType, block) {
        var classStr = STR_NULL;
        var uuid = block.getUUID();
        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-input-param-${index}-${uuid}`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.DEF) {
            classStr = `vp-nodeeditor-input-param-${index}-${uuid}'`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.RETURN 
                    || blockCodeType === BLOCK_CODELINE_TYPE.RETURN_SUB) {
            classStr = `vp-nodeeditor-input-param-${index}-${uuid}`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT) {
            classStr = `vp-nodeeditor-except-input-${uuid}`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.ELIF) {
            classStr = `vp-nodeeditor-elif-input-${uuid}`;
        }

        var inParamDom = $(`<div class='vp-nodeeditor-style-flex-row'
                                 style='margin-top:5px;'>

                                <div class='vp-nodeeditor-style-flex-column-center'
                                    style='margin:0 0.5rem; color: rgba(0,0,0,0.3);'>
                                    ${index+1}
                                </div>

                                <div class='vp-nodeeditor-blockoption-block
                                            vp-nodeeditor-blockoption-inner 
                                            vp-nodeeditor-style-flex-row' 
                                     style='position:relative; margin-top:0px;'>
                                    <input placeholder='input param' 
                                           class='vp-nodeeditor-blockoption-input ${classStr}' 
                                           value='${inParam}'>                                                        
                                </div>
                            </div>`);
        return inParamDom;
    }

    var renderBottomOptionTitle = function(title) {
        var titleDom = $(`<div class='vp-nodeeditor-option-container'
                               style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${title}</span>
                                    
                                </div>
                            </div>`);
        return titleDom;
    }

    var renderElseBlock = function(that, blockCodeType) {
        var name = '';
        if ( blockCodeType === BLOCK_CODELINE_TYPE.TRY) {
            name = 'finally';
        } else {
            name = 'else';
        }

        var isState;
        if ( blockCodeType === BLOCK_CODELINE_TYPE.IF) {
            isState = that.getState(STATE_isIfElse);
        } else if ( blockCodeType === BLOCK_CODELINE_TYPE.TRY) {
            isState = that.getState(STATE_isFinally);
        } else {
            isState = that.getState(STATE_isForElse);
        }
        
        var isTrueBorderStyle = '';
        var isFalseBorderStyle = '';
        if (isState === true ) {
            isTrueBorderStyle = `border: 2px solid yellow;`;
            isFalseBorderStyle = 'border: 2px solid black; background-color: white; color: black;';
        } else {
            isTrueBorderStyle = `border: 2px solid black; background-color: white; color: black;`;
            isFalseBorderStyle = `border: 2px solid yellow;`;
        }

        var uuid = that.getUUID();
        var elseBlock = $(`<div class='vp-nodeeditor-option-container'
                                style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${name}</span>
                                    <div class='vp-nodeeditor-style-flex-row-center'>

                                        <div style='display:flex; margin-right: 5px;'>
                                            <button class='vp-block-btn vp-nodeeditor-else-yes-${uuid}'
                                                    style='margin-right:5px; ${isTrueBorderStyle}'>
                                                yes
                                            </button>
                                        </div>

                                        <div style='display:flex;'>
                                            <button class='vp-block-btn vp-nodeeditor-else-no-${uuid}'
                                                    style=' ${isFalseBorderStyle}'>
                                                no
                                            </button>
                                        </div>

    
                                    </div>
                                </div>
                            </div>`);
        return elseBlock;
    }

    var renderDefaultOrDetailButton = function(that, uuid, blockCodeType) {
        var defaultOptionTitle = STR_NULL;
        var detailOptionTitle = STR_NULL;
        if (blockCodeType === BLOCK_CODELINE_TYPE.IMPORT) {
            defaultOptionTitle = `Default Import`;
            detailOptionTitle = `Custom Import`;
        } else {
            defaultOptionTitle = `Default Option`;
            detailOptionTitle = `Detail Option`; 
        }

        var isBaseImportPage = that.getState('isBaseImportPage');
        var defaultOrDetailButton = $(`<div class='vp-nodeeditor-style-flex-row-between'>
                                            <button class='vp-nodeeditor-default-option-${uuid} 
                                                           vp-nodeeditor-default-detail-option-btn
                                                           ${isBaseImportPage === true ? 'vp-nodeeditor-option-btn-selected': ''}'>
                                                    ${defaultOptionTitle}
                                            </button>
                                            <button class='vp-nodeeditor-detail-option-${uuid} 
                                                           vp-nodeeditor-default-detail-option-btn
                                                           ${isBaseImportPage === false ? 'vp-nodeeditor-option-btn-selected': ''}'>
                                                    ${detailOptionTitle}
                                            </button>
                                        </div>`);
        return defaultOrDetailButton;
    }

    /** 특정 input태그 값 입력 안 될시 빨간색 border 
     *  값 입력 x -> font-weight 300
     *  값 입력 o -> font-weight 799
     */
    var renderInputRequiredColor = function(that) {
        if ($(that).val() === STR_NULL) {
            $(that).css('font-weight', 300);
            $(that).addClass('vp-nodeeditor-option-input-required')
        } else {
            $(that).css('font-weight', 700);
            $(that).removeClass('vp-nodeeditor-option-input-required'); 
        }
    }

    var renderDeleteButton = function() {
        return $(`<button class='vp-block-btn'>x</button>`);
    }

    var renderCustomImportDom = function(customImportData, index) {
        const { isImport, baseImportName, baseAcronyms } = customImportData;
        var customImportDom = $(`<div class='vp-nodeeditor-style-flex-row-between'>
                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                        <input class='vp-nodeeditor-blockoption-custom-import-input
                                                      vp-nodeeditor-blockoption-custom-import-input-${index}' 
                                            
                                            type='checkbox' 
                                            ${isImport === true ? 'checked': ''}>
                                        </input>
                                    </div>
                                    <select class='vp-nodeeditor-select
                                                    vp-nodeeditor-blockoption-custom-import-select
                                                    vp-nodeeditor-blockoption-custom-import-select-${index}'
                                            style='margin-right:5px;'>
                                        <option value='numpy' ${baseImportName === 'numpy' ? STR_SELECTED : ''}>
                                            numpy
                                        </option>
                                        <option value='pandas' ${baseImportName === 'pandas' ? STR_SELECTED : ''}>
                                            pandas
                                        </option>
                                        <option value='matplotlib' ${baseImportName === 'matplotlib' ? STR_SELECTED : ''}>
                                            matplotlib
                                        </option>
                                        <option value='seaborn' ${baseImportName === 'seaborn' ? STR_SELECTED : ''}>
                                            seaborn
                                        </option>
                                        <option value='os' ${baseImportName === 'os' ? STR_SELECTED : ''}>
                                            os
                                        </option>
                                        <option value='sys' ${baseImportName === 'sys' ? STR_SELECTED : ''}>
                                            sys
                                        </option>
                                        <option value='time' ${baseImportName === 'time' ? STR_SELECTED : ''}>
                                            time
                                        </option>
                                        <option value='datetime' ${baseImportName === 'datetime' ? STR_SELECTED : ''}>
                                            datetime
                                        </option>
                                        <option value='random' ${baseImportName === 'random' ? STR_SELECTED : ''}>
                                            random
                                        </option>
                                        <option value='math' ${baseImportName === 'math' ? STR_SELECTED : ''}>
                                            math
                                        </option>
                                    </select>
                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                        <input class='vp-nodeeditor-blockoption-custom-import-textinput
                                                      vp-nodeeditor-blockoption-custom-import-textinput-${index}
                                                    ${baseAcronyms === '' ? 'vp-nodeeditor-option-input-required' : ''}'
                                                style='width: 90%;' 
                                                type='text' 
                                                placeholder='input import'
                                                value='${baseAcronyms}'></input>
                                    </div>
                                </div>`);
        return customImportDom;
    }

    var renderDefaultOrCustomImportContainer = function(importType, countisImport) {
        var name = STR_NULL;
        var customImportButton = STR_NULL;
        if (importType === IMPORT_BLOCK_TYPE.DEFAULT) {
            name = 'default';
        } else {
            name = 'custom';
            customImportButton = `<button class='vp-block-btn vp-nodeeditor-custom-import-plus-btn'
                                        style='margin-right:5px;'>
                                    + import
                                </button>`;
        }
        // <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
        var container = $(`<div class='vp-nodeeditor-blockoption-${name}-import-container'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${name}</span>
                                    <div class='vp-nodeeditor-style-flex-row-center'>
                                        <span class='vp-nodeeditor-${name}-import-number'
                                                style='margin-right:5px;'>
                                                ${countisImport} Selected
                                        </span>
                                            ${customImportButton}
                                       
                                    </div>
                                </div>
                            </div>`);

        return container;
    }

    var renderElifOrExceptContainer = function(blockCodeLineType, listData) {
        var name = STR_NULL;
        var blockName = STR_NULL;
        var blockOrCon = STR_NULL;
        if ( blockCodeLineType === BLOCK_CODELINE_TYPE.IF ) {
            name = 'con';
            blockName = 'if';
            blockOrCon = 'Condition';
        } else if ( blockCodeLineType === BLOCK_CODELINE_TYPE.ELIF ) {
            name = 'elif';
            blockName = 'elif';
            blockOrCon = 'Block';
        } else {
            name = 'except';
            blockName = 'except';
            blockOrCon = 'Block';
        }

        // <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
        var container = $(`<div class='vp-nodeeditor-option-container'
                                style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${blockName}</span>
                                        <div class='vp-nodeeditor-style-flex-row-center' >
                                            <span class='vp-nodeeditor-${name}-number
                                                         vp-nodeeditor-style-flex-column-center'
                                                  style='margin-right:5px;'>
                                                ${listData.length} ${blockOrCon}
                                            </span>
                                            <button class='vp-block-btn vp-nodeeditor-${blockName}-plus-btn'
                                                    style='margin-right:5px;'>
                                                + ${name}
                                            </button>
                                            <button class='vp-block-btn vp-nodeeditor-${blockName}-delete-btn'
                                                    style=''>
                                                - ${name}
                                            </button>
                                            
                                        </div>
                                    </div>
                            </div>`);
        return container;
    }

    var renderDefaultImportDom = function(baseImportData, index) {
        const { isImport, baseImportName, baseAcronyms } = baseImportData;
        var defaultImportDom = $(`<div class='vp-nodeeditor-style-flex-row-between'
                                        style='padding: 0.1rem 0;'>
                                        <div class='vp-nodeeditor-style-flex-column-center'>
                                            <input class='vp-nodeeditor-blockoption-default-import-input-${index}' 
                                                    type='checkbox' 
                                                    ${isImport === true ? 'checked': ''}>
                                            </input>
                                        </div>
                                        <div class='vp-nodeeditor-style-flex-column-center'>
                                            <span style='font-size:12px; font-weight:700;'> ${baseImportName}</span>
                                        </div>
                                        <div class='vp-nodeeditor-style-flex-column-center'
                                            style='width: 50%;     text-align: center;'>
                                            <span class=''>${baseAcronyms}</span>
                                
                                        </div>
                                </div>`);
        return defaultImportDom;
    }

    var renderDeleteBlockButton = function() {
        var deleteBtn = $(`<div class='vp-block-delete-btn
                                       vp-nodeeditor-style-flex-column-center'>
                                <i class="vp-fa fa fa-times vp-block-option-icon"></i>
                            </div>`);
        return deleteBtn;                     
    }

    var renderFocusedPage = function(focusedPageType) {
        $(VP_CLASS_NODEEDITOR_RIGHT).css(STR_BORDER, 'transparent');
        $(VP_CLASS_NODEEDITOR_RIGHT).css(`border-right`, '1px solid #d4d4d4');
        $(VP_CLASS_NODEEDITOR_RIGHT).css(`border-top-left-radius`, '7px');
        $(VP_CLASS_NODEEDITOR_RIGHT).css(`border-bottom-left-radius`, '7px');

        $(VP_CLASS_NODEEDITOR_LEFT).css(STR_BORDER, 'transparent');
        $(VP_CLASS_NODEEDITOR_LEFT).css(`border-right`, '1px solid #d4d4d4');

        $(VP_CLASS_NODEEDITOR_OPTION_TAB).css(STR_BORDER, 'transparent');
        $(VP_CLASS_NODEEDITOR_OPTION_TAB).css(`border-top-right-radius`, '7px');
        $(VP_CLASS_NODEEDITOR_OPTION_TAB).css(`border-bottom-right-radius`, '7px');
        
        if ( focusedPageType === FOCUSED_PAGE_TYPE.BUTTONS ) {
            $(VP_CLASS_NODEEDITOR_RIGHT).css(STR_BORDER, `3px ${COLOR_FOCUSED_PAGE} solid`);
        } else if (focusedPageType === FOCUSED_PAGE_TYPE.EDITOR) {
            $(VP_CLASS_NODEEDITOR_LEFT).css(STR_BORDER, `3px ${COLOR_FOCUSED_PAGE} solid`);
        } else if (focusedPageType === FOCUSED_PAGE_TYPE.OPTION) {
            $(VP_CLASS_NODEEDITOR_OPTION_TAB).css(STR_BORDER, `3px ${COLOR_FOCUSED_PAGE} solid`);
        } else {

        }
    }

    var renderOptionTitle = function(thatBlock) {
        var blockCodeLineName = thatBlock.getBlockName();
        blockCodeLineName = blockCodeLineName.charAt(0).toUpperCase() + blockCodeLineName.slice(1)
        var optionTitle = $(`<div class='vp-nodeeditor-tab-navigation-node-childs-option-title'>
                                <div class='vp-nodeeditor-panel-area-vertical-btn2
                                            vp-nodeeditor-panel-area-vertical-btn2-${thatBlock.getUUID()}
                                            vp-nodeeditor-arrow-up'>▲</div>
                                    <span class='vp-block-blocktab-name 
                                                    vp-block-blocktab-name-title'
                                            style="font-size: 16px;">${blockCodeLineName} Option</span>
                                
                           </div>`);

        return optionTitle;
    }

    var renderPropertyDom = function(that) {
        var uuid = that.getUUID();
        var blockContainerThis = that.getBlockContainerThis();
        var propertyCodeLineState = that.getState(STATE_propertyCodeLine);
        var index = propertyCodeLineState.indexOf('@');
        var newPropertyCodeLineState = propertyCodeLineState.slice(0, index) + propertyCodeLineState.slice(index+1, propertyCodeLineState.length);
        var propertyDom = $(`<div class='vp-block-blockoption 
                                         vp-nodeeditor-blockoption-block 
                                         vp-nodeeditor-blockoption-inner 
                                         vp-nodeeditor-style-flex-row-between' 
                                  style='position: relative;'>
                    
                                <span class='vp-nodeeditor-style-flex-column-center'
                                      style='margin-right: 5px;'>
                                    @
                                </span>                                     
                            </div>`);

        var inputDom = $(`<input class='vp-nodeeditor-blockoption-input
                                        vp-nodeeditor-property-input-${uuid}'
                                style='width:90%; margin-right: 5px;' 
                                value="${newPropertyCodeLineState}"
                                placeholder='input property' ></input> `);
        var resetButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>Reset</button>`);

        $(resetButton).click(function() {                                    
            that.setState({
                propertyCodeLine: '@property'
            });
            $(`.vp-nodeeditor-property-input-${uuid}`).html('property');
            $(`.vp-block-header-property-${that.getUUID()}`).html(that.getState(STATE_propertyCodeLine));
            blockContainerThis.renderBlockOptionTab();
        });

        propertyDom.append(inputDom);
        propertyDom.append(resetButton);
        return propertyDom;                                        
    };
    
    var renderPropertyDomFromDef = function(that) {
        var blockContainerThis = that.getBlockContainerThis();
        var uuid = that.getUUID();
        var propertyBlock = null;
        var propertyCodeLineState = STR_NULL;

        /** def block 바로 위에 property block이 있을 경우 */
        if (that.getPrevBlock() && that.getPrevBlock().getBlockCodeLineType() === BLOCK_CODELINE_TYPE.PROPERTY ) {
            that.setPropertyBlockFromDef(that.getPrevBlock());
            propertyBlock = that.getPropertyBlockFromDef();
            propertyCodeLineState = propertyBlock.getState(STATE_propertyCodeLine);
        /** def block 바로 위에 property block이 없을 경우 */      
        } else {
            that.setPropertyBlockFromDef(null);
        }

        var index = propertyCodeLineState.indexOf('@');
        var newPropertyCodeLineState = propertyCodeLineState.slice(0, index) + propertyCodeLineState.slice(index+1, propertyCodeLineState.length);

        var propertyDom = $(`<div class='vp-block-blockoption 
                                         vp-nodeeditor-blockoption-block 
                                         vp-nodeeditor-blockoption-inner 
                                         vp-nodeeditor-style-flex-row-end' 
                                  style='position: relative;'>
                                <span class='vp-block-optiontab-name 
                                             vp-nodeeditor-style-flex-column-center'
                                      style='margin-right: 5px;'>
                                    Property
                                </span>     
                                <span class='vp-nodeeditor-style-flex-column-center'
                                      style='margin-right: 5px;'>
                                    @
                                </span>                                     
                            </div>`);

        var inputDom = $(`<input class='vp-nodeeditor-blockoption-input
                                        vp-nodeeditor-defproperty-input-${uuid}'
                                style='width:25%; margin-right: 5px;' 
                                value="${newPropertyCodeLineState}"
                                placeholder='input' ></input> `);
        var clearButton = $(`<button class='vp-nodeeditor-option-reset-button 
                                            vp-block-btn'>x</button>`);
        $(clearButton).click(function() {
            var propertyBlock = that.getPropertyBlockFromDef();
            if (propertyBlock) {
                propertyBlock.deleteLowerDepthChildBlocks();
            }
            blockContainerThis.renderBlockOptionTab();
     
        });     

        propertyDom.append(inputDom);
        propertyDom.append(clearButton);
        return propertyDom;           
    }

    var renderClassParentDom = function(that) {
        var uuid = that.getUUID();
        var parentClassName = that.getState(STATE_classInParamList)[0];

        var name = 'Parent class';
        var classStr = `vp-nodeeditor-input-param-${0}-${uuid}`;
        var inputStyleStr = 'width:66%;';


        var nameDom = $(`<div class='vp-block-blockoption 
                                        vp-nodeeditor-blockoption-block 
                                        vp-nodeeditor-blockoption-inner 
                                        vp-nodeeditor-style-flex-row-between' 
                                style='position:relative;'>
                                <span class='vp-block-optiontab-name 
                                             vp-nodeeditor-style-flex-column-center'>${name}</span>
                                <input class='vp-nodeeditor-blockoption-input 
                                              ${classStr}'
                                    style='${inputStyleStr}' 
                                    value="${parentClassName}"
                                    placeholder='input parent class' ></input>   
                                                                                
                                </div>`);
        return nameDom;
    }

    var renderPureDom = function() {

    }

    return {
        renderMainDom
        , renderLeftHolderDom
        , renderMainInnerDom
        , renderMainHeaderDom
        , renderDefaultImportDom
        , renderCustomImportDom 

        , renderBottomOptionContainer
        , renderBottomOptionContainerInner
        , renderDefaultOrCustomImportContainer
        , renderElifOrExceptContainer
        , renderInParamContainer
        , renderDefParamDom
        , renderInParamDom

        , renderBottomOptionInnerDom
        , renderBottomOptionName
        , renderDomContainer
      
        , renderBottomOptionTitle
        , renderElseBlock

        , renderDefaultOrDetailButton
        , renderDeleteButton
        , renderDeleteBlockButton
        , renderFocusedPage

        , renderInputRequiredColor
        , renderOptionTitle
        , renderPropertyDom
        , renderPropertyDomFromDef
        , renderIfConditionDom
        , renderClassParentDom

        , generateClassInParamList
        , generateDefInParamList
        , generateReturnOutParamList
        , generateIfConditionList
    }
});
