define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , './api.js'
    , './config.js'
    , './constData.js'
    , './block.js'
    , './blockRenderer.js'
], function (vpCommon, vpFuncJS, api, config, constData, block, blockRenderer ) {
    const { changeOldToNewState
            , makeFirstCharToUpperCase
            , findStateValue
            , mapTypeToName } = api;
    const { PROCESS_MODE } = config;
    const {  BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK
            , FOCUSED_PAGE_TYPE

            , STR_CHANGE_KEYUP_PASTE
            , STR_COLON_SELECTED 

            , VP_CLASS_BLOCK_NUM_INFO
            , VP_CLASS_BLOCK_CONTAINER
            , VP_CLASS_NODEEDITOR_LEFT

            , VP_CLASS_BLOCK_HEADER_PARAM
            , VP_CLASS_NODEEDITOR_INPUT_PARAM
            , VP_CLASS_NODEEDITOR_PARAM_PLUS_BTN
            , VP_CLASS_NODEEDITOR_PARAM_DELETE_BTN

            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_DEFAULT_POS_Y
            , NUM_DEFAULT_POS_X

            , STR_NULL
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_ONE_SPACE
            , STR_DOT
            , STR_SCROLLHEIGHT
            , STR_DATA_NUM_ID
            , STR_PX
            , STR_BORDER

            , STR_COLOR
            , STR_DATA_DEPTH_ID 

            , STATE_classInParamList
            , STATE_defInParamList
            , STATE_returnOutParamList

            , STATE_elifCodeLine
            , STATE_exceptCodeLine

            , STATE_breakCodeLine
            , STATE_continueCodeLine
            , STATE_passCodeLine
            , STATE_customCodeLine
            , STATE_propertyCodeLine
   

            , STATE_isIfElse
            , STATE_isForElse
            , STATE_isFinally

            , COLOR_ORANGE
            , COLOR_BLOCK_YELLOW
            , COLOR_SKY_BLUE
            , COLOR_FOCUSED_PAGE

            , API_BLOCK_PROCESS_DEVELOPMENT } = constData;
 
    const { mapTypeToBlock } = block;
    const { generateClassInParamList 
            , generateDefInParamList
            , generateReturnOutParamList
            , renderInputRequiredColor
            , renderFocusedPage } = blockRenderer;

    var BlockContainer = function() {
        this.importPackageThis = null;
        this.blockList = [];
        this.blockHistoryStack = [];

        this.resetBlockListButton = null;

        this.isDebugMode = false; 
        this.focusedPageType = FOCUSED_PAGE_TYPE;
        this.classNum = 1;
        this.defNum = 1;
        this.forNum = 1;
        this.thisBlockFromRootBlockHeight = 0;
        this.eventClientY = 0;

        this.isBlockDoubleClicked = false;
        this.code = STR_NULL;
    }

    BlockContainer.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    BlockContainer.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    BlockContainer.prototype.setIsBlockDoubleClicked = function(isBlockDoubleClicked) {
        this.isBlockDoubleClicked = isBlockDoubleClicked;
    }

    BlockContainer.prototype.getIsBlockDoubleClicked = function() {
        return this.isBlockDoubleClicked;
    }
    /** 현재 API Block에 존재하는 블럭을 위에서 부터 맨 아래까지 traverse 하면서 console.log 찍는다. */
    BlockContainer.prototype.traverseBlockList = function() {
        var that = this;
        var blockList = this.blockList;
        var rootBlockList = [];
        blockList.forEach(block => {
            if (block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER ) {
                return;
            }
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {
    
            } else {
                rootBlockList.push(rootBlock);
            }
        });
    
        rootBlockList.forEach(rootBlock => {
            /**  */
            var nextBlockList = rootBlock.getNextBlockList();
            var stack = [];
    
            if (nextBlockList.length !== 0) {
                stack.push(nextBlockList);
            }

            console.log(0,'blockName : ', rootBlock.getBlockName(), 'direction', rootBlock.getDirection());
            var travelBlockList = [rootBlock];
       
            var iteration = 0;
            var current;
            while (stack.length !== 0) {
                current = stack.shift();
                /** FIXME: 무한루프 체크 */
             
                if (iteration > NUM_MAX_ITERATION) {
                    console.log('무한루프');
                    break;
                }
    
                /** 배열 일 때 */
                if (Array.isArray(current)) {
                    var tempList = [];
                    current.forEach(element => {
                        tempList.push(element);
                    });
                    
                    tempList = tempList.sort((a,b) => {
                        if (a.getDirection() === BLOCK_DIRECTION.INDENT) {
                            return 1;
                        } else {
                            return -1;
                        }
                    });
                    tempList.forEach(el => {
                        stack.unshift(el);
                    });
                } else {
                    iteration++;
                    var currBlock = current;
                    // var direction = current.getDirection();
                    // var newData = {
                    //     currBlock
                    //     , direction
                    // }

                    if ( currBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER ) {
                        console.log(iteration, 'blockName : ', currBlock.getSupportingBlock().getBlockName(), 'holder', 'direction', currBlock.getDirection());
                    } else {
                        console.log(iteration, 'blockName : ', currBlock.getBlockName(), 'direction', currBlock.getDirection());
                    }

               
                    if (currBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER) {
                    } else {
                        travelBlockList.push(currBlock);
                    }
    
                    var nextBlockDataList = current.getNextBlockList();
                    stack.unshift(nextBlockDataList);
                }
            }
            // console.log('----------------------------------');
            var iteration = 0;
            travelBlockList.some(block => {
                iteration++;
                if (iteration > NUM_MAX_ITERATION) {
                    console.log('무한루프');
                    return true;
                }
                // console.log('name : ', block.getBlockName());
            });
            console.log('travelBlockList', travelBlockList);
        });
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addBlock = function(block) {
        this.blockList = [...this.blockList, block];
    }

    /** blockList를 가져옴*/
    BlockContainer.prototype.getBlockList = function() {
        return this.blockList;
    }
    /** blockList를 파라미터로 받은 blockList로 덮어 씌움*/
    BlockContainer.prototype.setBlockList = function(blockList) {
        this.blockList = blockList;
    }

    /** blockHistoryStack를 가져옴*/
    BlockContainer.prototype.getBlockHistoryStack = function() {
        return this.blockHistoryStack;
    }
    /** blockHistoryStack를 파라미터로 받은 blockHistoryStack로 덮어 씌움*/
    BlockContainer.prototype.setBlockHistoryStack = function(blockHistoryStack) {
        this.blockHistoryStack = blockHistoryStack;
    }

    BlockContainer.prototype.pushBlockHistoryStack = function(blockStack) {
        this.blockHistoryStack.push(blockStack);
    }

    /** blockHistoryStack에 최신 데이터를 pop합니다 */
    BlockContainer.prototype.popBlockHistoryStackAndGet = function() {
        if (this.blockHistoryStack.length < 1) {
            return;
        }
        return this.blockHistoryStack.pop();
    }
    /** blockHistoryStack을 리셋합니다  */
    BlockContainer.prototype.resetStack = function() {
        this.blockHistoryStack = [];
    }

    BlockContainer.prototype.getRootBlockList = function() {
        var blockList = this.getBlockList();

        var rootBlockList = [];

        blockList.forEach(block => {
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {
            } else {
                rootBlockList.push(rootBlock);
            }
        });
        return rootBlockList;
    }
    BlockContainer.prototype.getRootBlock = function() {
        var rootBlockList = this.getRootBlockList();
        return rootBlockList[0];
    }

    BlockContainer.prototype.getCtrlPressedBlockList = function() {
        var ctrlPressedBlockList = [];
        var blockList = this.getBlockList();
        blockList.forEach(block => {
            if ( block.getIsCtrlPressed() === true) {
                ctrlPressedBlockList.push(block);
            }
        });
        return ctrlPressedBlockList;
    }

    BlockContainer.prototype.setClassNum = function(classNum) {
        this.classNum = classNum;
    }
    BlockContainer.prototype.addClassNum = function() {
        this.classNum += 1;
    }
    BlockContainer.prototype.getClassNum = function() {
        return this.classNum;
    }

    BlockContainer.prototype.setDefNum = function(defNum) {
        this.defNum = defNum;
    }
    BlockContainer.prototype.addDefNum = function() {
        this.defNum += 1;
    }
    BlockContainer.prototype.getDefNum = function() {
        return this.defNum;
    }

    BlockContainer.prototype.setForNum = function(forNum) {
        this.forNum = forNum;
    }
    BlockContainer.prototype.addForNum = function() {
        this.forNum += 1;
    }
    BlockContainer.prototype.getForNum = function() {
        return this.forNum;
    }

    BlockContainer.prototype.getMaxWidth = function() {
        var maxWidth = $(VP_CLASS_NODEEDITOR_LEFT).width();
        return maxWidth;
    }

    BlockContainer.prototype.getMaxHeight = function() {
        var maxHeight = $(VP_CLASS_NODEEDITOR_LEFT).height();
        return maxHeight;
    }

    BlockContainer.prototype.getScrollHeight = function() {
        var scrollHeight = $(VP_CLASS_NODEEDITOR_LEFT).prop(STR_SCROLLHEIGHT);
        return scrollHeight;
    }

    BlockContainer.prototype.setThisBlockFromRootBlockHeight = function(thisBlockFromRootBlockHeight) {
        this.thisBlockFromRootBlockHeight = thisBlockFromRootBlockHeight;
    }
    BlockContainer.prototype.getThisBlockFromRootBlockHeight = function() {
        return this.thisBlockFromRootBlockHeight;
    }

    BlockContainer.prototype.setEventClientY = function(eventClientY) {
        this.eventClientY = eventClientY;
    }
    BlockContainer.prototype.getEventClientY = function() {
        return this.eventClientY;
    }

    BlockContainer.prototype.setResetBlockListButton = function(resetBlockListButton) {
        this.resetBlockListButton = resetBlockListButton;
    }
    BlockContainer.prototype.getResetBlockListButton = function() {
        return this.resetBlockListButton;
    }
    /** blockList에서 특정 block을 삭제
     * @param {string} blockUUID
     */
    BlockContainer.prototype.deleteBlock = function(blockUUID) {
        var selectedIndex = -1;
    
        /** blockList를 돌며 삭제하고자 하는 block을 찾음.
         *  block은 고유의 UUID 
         *  파라미터로 들어온 block의 UUID가 blockList의 UUID와 일치하는 블럭이 있는지 찾는 과정.
         *  찾으면 isBlock true, blockList에서 index를 얻음
         *  못찾으면 isBlock false, 아무것도 하지 않고 메소드 작업을 종료.
         */
        var blockList = this.getBlockList();
        var isBlock = blockList.some((block, index) => {
            if (block.getUUID() === blockUUID) {
                selectedIndex = index;
                return true;
            } else {
                return false;
            }
        });
    
        if (isBlock) {
            var selectedBlock = blockList[selectedIndex];
    
            blockList.splice(selectedIndex,1);
    
            if ( selectedBlock.getFirstIndentBlock() ) {
                blockList.some((block, index) => {
                    if (selectedBlock.getFirstIndentBlock().getUUID() === block.getUUID()) {
                        blockList.splice(index, 1);
                        return true;
                    }
                });
            }
    
            if ( selectedBlock.getHolderBlock() ) {
                blockList.some((block, index) => {
                    if (selectedBlock.getHolderBlock().getUUID() === block.getUUID()) {
                        blockList.splice(index, 1);
                        return true;
                    }
                });
            }
        } 
    }

    /**
     * Block list의 state 데이터를 json 으로 변환하는 메소드
     */
    BlockContainer.prototype.mapBlockListDataToBlockJson = function() {
        var rootBlock = this.getRootBlock();
        /**  */
        var nextBlockList = rootBlock.getNextBlockList();
        var stack = [];

        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }
        var uuid = rootBlock.getUUID();
        var depth = rootBlock.getDepth();
        var direction = rootBlock.getDirection();
        var blockCodeLineType = rootBlock.getBlockCodeLineType();
        var blockName = rootBlock.getBlockName();
        var codeLine = rootBlock.getCodeLine();
        var nextBlockList = rootBlock.getNextBlockList();

        var tempBlockData = {
            uuid
            , depth
            , blockCodeLineType
            , blockName
            , direction
            , codeLine
            , nextBlockList
        }
        var travelBlockList = [tempBlockData];

        var iteration = 0;
        var current;
        while (stack.length !== 0) {
            current = stack.shift();
            iteration++;
            if (iteration > NUM_MAX_ITERATION) {
                console.log('무한루프');
                break;
            }
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                var temp = [];
                current.forEach(element => {
                    temp.push(element);
                });
                
                temp = temp.sort((a,b) => {
                    // console.log('a',a);
                    if (a.getDirection() === BLOCK_DIRECTION.INDENT) {
                        return 1;
                    } else {
                        return -1;
                    }
                });
                temp.forEach(el => {
                    stack.unshift(el);
                });


            } else {
    
                var uuid = current.getUUID();
                var depth = current.getDepth();
                var direction = current.getDirection();
                var blockCodeLineType = current.getBlockCodeLineType();
                var blockName = current.getBlockName();
                var codeLine = current.getCodeLine();
                var nextBlockList = [...current.getNextBlockList()];
                stack.unshift([...nextBlockList]);

                var blockData = {
                    uuid
                    , depth
                    , blockCodeLineType
                    , blockName
                    , direction
                    , codeLine
                    , nextBlockList
                }
                if (current.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER ) {

                } else {
                    tempBlockData.nextBlockList = [];
                    var is = travelBlockList.some(travelBlock => {
                        if (current.getDirection() === BLOCK_DIRECTION.DOWN
                            && current.getPrevBlock().getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER 
                            && current.getPrevBlock().getPrevBlock().getUUID() === travelBlock.uuid) {
                            blockData.nextBlockList = [];

                            var is = travelBlock.nextBlockList.some(nextBlock => {
                                if (nextBlock.uuid === blockData.uuid) {
                                    return true;
                                }
                            });
                            if (is === false) {
                                travelBlock.nextBlockList.push(blockData);
                            }
                        }
                    });
                 
                  
                    if (tempBlockData.depth <= blockData.depth) {
                        var is = tempBlockData.nextBlockList.some(nextBlock => {
                            if (nextBlock.uuid === blockData.uuid) {
                                return true;
                            }
                        });
                        if (is === false) {
                            tempBlockData.nextBlockList.push(blockData);
                        }
                    }
                    travelBlockList.forEach(travelBlock => {
                        // console.log('tempBlockData.nextBlockList', travelBlock.nextBlockList);
                    });
                 
                    tempBlockData = blockData;
                    travelBlockList.push(blockData); 
                }

            }
        }

        this.mapBlockJsonToBlockListData(travelBlockList[0]);
        return travelBlockList[0];
    }

    /**
     * @param {Object} blockJson 
     */
    BlockContainer.prototype.mapBlockJsonToBlockListData = function(blockJson) {
        // var rootBlock = this.getRootBlock();
        // rootBlock.deleteBlock();
        // console.log('blockJson', blockJson);

        var uuid = blockJson.uuid;
        var direction = blockJson.direction;
        var blockName = blockJson.blockName;
        var codeLine = blockJson.codeLine;
        var nextBlockList = blockJson.nextBlockList;
        var blockCodeLineType = blockJson.blockCodeLineType;

        // console.log('direction',direction, 'blockName',blockName, 'codeLine',codeLine, 'nextBlockList', nextBlockList, 'uuid', uuid);

        // var newBlockList = [];
        // var block = mapTypeToBlock(this, blockCodeLineType , {pointX: 0, pointY: 0});
        // this.reRenderBlockList();
        // newBlockList.push(block);

        var stack = [nextBlockList];
        var current;
        var iteration = 0;
        while (stack.length !== 0) {
            current = stack.shift();
            iteration++;
            if (iteration > NUM_MAX_ITERATION) {
                console.log('무한루프');
                break;
            }

            /** 배열 일 때 */
            if (Array.isArray(current)) {
                var temp = [];
                current.forEach(element => {
                    temp.push(element);
                });
                
                temp = temp.sort((a,b) => {
                    if (a.direction === BLOCK_DIRECTION.INDENT) {
                        return 1;
                    } else {
                        return -1;
                    }
                });
                temp.forEach(el => {
                    stack.unshift(el);
                });


            } else {
                var uuid = current.uuid;
                var direction = current.direction;
                var blockName = current.blockName;
                var codeLine = current.codeLine;
                var nextBlockList = current.nextBlockList;
                var blockCodeLineType = current.blockCodeLineType;
                // console.log('direction',direction, 'blockName',blockName, 'codeLine',codeLine, 'nextBlockList', nextBlockList, 'uuid', uuid);
                stack.unshift(nextBlockList);
            }
        }
    }
    
    /** API Block 화면에 조립된 Block의 정렬 순서와 값들을 토대로 Jupyter cell에 코드를 생성하는 메소드 */
    BlockContainer.prototype.makeCode = function() {
        var that = this;
        var blockList = this.getBlockList();
        var rootBlockList = [];
        blockList.forEach(block => {
            if (block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER) {
                return;
            }
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {

            } else {
                rootBlockList.push(rootBlock);
            }
        });

        var codeLineStrDataList = [];
        var codeLineStr = STR_NULL;
        rootBlockList.forEach(rootBlock => {
            
            /**  */
            var nextBlockList = rootBlock.getNextBlockList();
            var stack = [];

            if (nextBlockList.length !== 0) {
                stack.push(nextBlockList);
            }

            var travelBlockList = [rootBlock];

            var iteration = 0;
            var current;
            while (stack.length !== 0) {
                current = stack.shift();
                iteration++;
                if (iteration > 1000) {
                    console.log('무한루프');
                    break;
                }
                /** 배열 일 때 */
                if (Array.isArray(current)) {
                    var temp = [];
                    current.forEach(element => {
                        temp.push(element);
                    });
                    
                    temp = temp.sort((a,b) => {
                        if (a.getDirection() === BLOCK_DIRECTION.INDENT) {
                            return 1;
                        } else {
                            return -1;
                        }
                    });
                    temp.forEach(el => {
                        stack.unshift(el);
                    });
    

                } else {
                    var currBlock = current;
                    var direction = current.getDirection();
                    var newData = {
                        currBlock
                        , direction
                    }
                    if (currBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER) {

                    } else {
                        travelBlockList.push(newData);
                    }

                    var nextBlockDataList = current.getNextBlockList();
                    stack.unshift(nextBlockDataList);
                }
            }

            travelBlockList.some((travelBlockData, index) => {
                var depth = 0;
    
                var blockName = STR_NULL;
                var direction = STR_NULL;
    
                var currBlock;
                // root 블럭일 경우
                if (index === 0) {
                    currBlock = travelBlockData;
                    blockName = travelBlockData.getBlockName();
        
                    travelBlockData.setDirection(BLOCK_DIRECTION.ROOT);
                } else {
                    currBlock = travelBlockData.currBlock;
                    blockName = travelBlockData.currBlock.getBlockName();
                    direction = travelBlockData.direction;

                    travelBlockData.currBlock.getDirection(direction);
         
                    if (direction === BLOCK_DIRECTION.INDENT) {
                        var prevBlock = travelBlockData.currBlock;
                        while (prevBlock.getPrevBlock() !== null) {
                            prevBlock = prevBlock.getPrevBlock();
                            if (prevBlock.getDirection() === BLOCK_DIRECTION.DOWN ) {
                    
                            } else {
                                depth++;
                            }
                        }
                    } else {
                        var prevBlock = travelBlockData.currBlock;
                        while (prevBlock.getPrevBlock() !== null) {
                            prevBlock = prevBlock.getPrevBlock();
                            if (prevBlock.getDirection() === BLOCK_DIRECTION.INDENT) {
                                depth++;
                            } else {
                        
                            }
                        }
                    }
                }

                /** depth 계산 */
                var _depth = depth;
                var indentString = STR_NULL;
                while (_depth-- !== 0) {
                    indentString += `    `;
                }

                var codeLine = currBlock.setCodeLineAndGet(indentString);
                codeLine += `\n`;
                codeLineStr += codeLine;
            });

            codeLineStrDataList.push({
                pointY: rootBlock.getContainerPointY()
                , codeLineStr
            });
            codeLineStr = ``;
        });

        codeLineStrDataList = codeLineStrDataList.sort((a,b) => {
            if (a.pointY - b.pointY > 0) {
                return 1;
            } else {
                return -1;
            }
        });

        var returnCodeLineStr = ``;
        returnCodeLineStr += `# Auto-Generated by VisualPython\n`;
        codeLineStrDataList.forEach((codeLineStrData, index) => {
            returnCodeLineStr += `${codeLineStrData.codeLineStr}\n`;
        });
        this.setAPIBlockCode(returnCodeLineStr);

        return returnCodeLineStr;
    }

    BlockContainer.prototype.getAPIBlockCode = function() {
        return this.code;
    }
    BlockContainer.prototype.setAPIBlockCode = function(code) {
        this.code = code;
    }

    /** block 이동시 block 왼쪽 지렛대의 height를 생성 */
    BlockContainer.prototype.renderBlockLeftHolderListHeight = function() {
        var blockList = this.getBlockList();
        var selectedBlockList = [];

        blockList.forEach(block => {
            var type = block.getBlockCodeLineType();
            if (type === BLOCK_CODELINE_TYPE.CLASS || type === BLOCK_CODELINE_TYPE.DEF || type === BLOCK_CODELINE_TYPE.IF ||
                type === BLOCK_CODELINE_TYPE.FOR || type === BLOCK_CODELINE_TYPE.WHILE || type === BLOCK_CODELINE_TYPE.TRY ||
                type === BLOCK_CODELINE_TYPE.ELSE || type === BLOCK_CODELINE_TYPE.ELIF || type === BLOCK_CODELINE_TYPE.FOR_ELSE || 
                type === BLOCK_CODELINE_TYPE.EXCEPT || type === BLOCK_CODELINE_TYPE.FINALLY ) {
                selectedBlockList.push(block);
            }
        });

        selectedBlockList.forEach(block => {
          
            if (block.getBlockLeftHolderDom()) {
                var leftHolderClientRect = $(block.getBlockLeftHolderDom())[0].getBoundingClientRect();

                var holderBlock = block.getHolderBlock();
                var holderBlockClientRect = $(holderBlock.getBlockMainDom())[0].getBoundingClientRect();
                // var mainDom = block.getBlockMainDom();
                // console.log('holderBlockClientRect', holderBlockClientRect);
                // console.log('leftHolderClientRect', leftHolderClientRect);
                // console.log('distance',block.getBlockName(), parseInt(distance));
                var distance = holderBlockClientRect.y - leftHolderClientRect.y;
                

            
                $(block.getBlockLeftHolderDom()).css('height',`${distance}px`);
                block.setTempBlockLeftHolderHeight(distance);
            }
        });
    }

    BlockContainer.prototype.setFocusedPageType = function(focusedPageType) {
        this.focusedPageType = focusedPageType;
    }
    BlockContainer.prototype.getFocusedPageType = function() {
        return this.focusedPageType;
    }
    BlockContainer.prototype.setFocusedPageTypeAndRender = function(focusedPageType) {
        this.setFocusedPageType(focusedPageType);
        renderFocusedPage(focusedPageType);
    }

    /** Block editor에 존재하는 블럭들을 전부 다시 렌더링한다 */
    BlockContainer.prototype.reRenderBlockList = function() {
  
        var rootBlock = this.getRootBlock();
        if (!rootBlock){
            return;
        }

        {
            var _containerDom = rootBlock.getContainerDom();
            $(_containerDom).empty();
            $(_containerDom).remove();
        }

        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);

        rootBlock.setContainerDom(containerDom);
        
        $(containerDom).css(STR_TOP, `${NUM_DEFAULT_POS_Y}` + STR_PX);
        $(containerDom).css(STR_LEFT, `${NUM_DEFAULT_POS_X}` + STR_PX);

        var blockChildList = rootBlock.renderChildBlockListIndentAndGet();
        blockChildList.forEach((block, index) => {
            var blockMainDom = block.getBlockMainDom();
            $(containerDom).append(blockMainDom);
            block.bindEventAll();
        });
 
        $(VP_CLASS_NODEEDITOR_LEFT).append(containerDom);
    }
    
    /** Block 앞에 line number를 오름차순으로 정렬한다 */
    BlockContainer.prototype.renderBlockLineNumberInfoDom_sortBlockLineAsc = function() {

        var rootBlock = this.getRootBlock();
        var blockChildList = rootBlock.getChildBlockList();
        var minusIndex = 0;

        blockChildList.forEach((block, index) => {

            var mainDom = block.getBlockMainDom();
            $(mainDom).css(STR_TOP,`${0}` + STR_PX);
            $(mainDom).css(STR_LEFT,`${0}` + STR_PX);
  
            $(mainDom).find(STR_DOT + VP_CLASS_BLOCK_NUM_INFO).remove();
            $(mainDom).find(STR_DOT + VP_CLASS_BLOCK_NUM_INFO).empty();

            if (block.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER) {
                // var blockDepth = block.getDepth();
                var blockDepth = parseInt( $(block.getBlockMainDom()).attr(STR_DATA_DEPTH_ID) );
                var blockLineNumber = index - minusIndex;

                var blockLineNumberInfoDom = document.createElement('span');
                blockLineNumberInfoDom.classList.add(VP_CLASS_BLOCK_NUM_INFO);

                $(mainDom).attr(STR_DATA_NUM_ID,`${blockLineNumber}`);
                $(blockLineNumberInfoDom).text(`[${blockLineNumber}] :`);

                var numberPx = -(NUM_INDENT_DEPTH_PX * blockDepth + NUM_DEFAULT_POS_X - 3);

                $(blockLineNumberInfoDom).css( STR_LEFT, `${numberPx}`+ STR_PX );
                $(mainDom).append(blockLineNumberInfoDom);
                block.setBlockNumber(blockLineNumber);

                block.setIsMoved(false);
            } else {
                /** 그림자 블럭(holder block)이 나오면 다음번 블럭의 index 계산 할때,
                 *  지금 까지 그림자 블럭(holder block) 나온 횟수 만큼 감소 
                 */
                minusIndex++;
            }
        });
    }


    /** Block 앞에 line number를 처음 생성된 시점의 line number를 유지한다 */
    BlockContainer.prototype.renderBlockLineNumberInfoDom = function() {

        var rootBlock = this.getRootBlock();
        var blockChildList = rootBlock.getChildBlockList();
        var minusIndex = 0;
        blockChildList.forEach((block, index) => {
            var mainDom = block.getBlockMainDom();
            $(mainDom).css(STR_TOP,`${0}` + STR_PX);
            $(mainDom).css(STR_LEFT,`${0}` + STR_PX);
     

            $(mainDom).find(STR_DOT + VP_CLASS_BLOCK_NUM_INFO).remove();
            $(mainDom).find(STR_DOT + VP_CLASS_BLOCK_NUM_INFO).empty();

            if (block.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER) {
                // var blockDepth = block.getDepth();
                var blockDepth = parseInt( $(block.getBlockMainDom()).attr(STR_DATA_DEPTH_ID) );
            
                var blockLineNumberInfoDom = document.createElement('span');
                blockLineNumberInfoDom.classList.add(VP_CLASS_BLOCK_NUM_INFO);

                var blockLineNumber = block.getBlockNumber();
                // console.log('blockLineNumber', blockLineNumber);

                $(mainDom).attr(STR_DATA_NUM_ID,`${blockLineNumber}`);
                $(blockLineNumberInfoDom).text(`[${blockLineNumber}] :`);

                var numberPx = -(NUM_INDENT_DEPTH_PX * blockDepth + NUM_DEFAULT_POS_X - 3);

                $(blockLineNumberInfoDom).css( STR_LEFT, `${numberPx}`+ STR_PX );
                if ( block.getIsMoved() === true ) {
                    $(blockLineNumberInfoDom).css(STR_COLOR, COLOR_FOCUSED_PAGE);
                }

                $(mainDom).append(blockLineNumberInfoDom);

            } else {
                /** 그림자 블럭(holder block)이 나오면 다음번 블럭의 index 계산 할때,
                 *  지금 까지 그림자 블럭(holder block) 나온 횟수 만큼 감소 
                 */
                minusIndex++;
            }
        });
    }
    /**
     * @param {BLOCK} checkBlock 
     */
    BlockContainer.prototype.getRootToLastBottomBlock = function(checkBlock) {
        var rootBlockList = this.getRootBlockList();
        var rootBlock = rootBlockList[0];

        return this.getLastBottomBlock(rootBlock, checkBlock);
    }

    /**
     * @param {BLOCK} thatBlock 
     * @param {BLOCK} checkBlock 
     */
    BlockContainer.prototype.getLastBottomBlock = function(thatBlock, checkBlock) {
        var nextBlockList = thatBlock.getNextBlockList();
        var stack = [];
        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }

        var current = null;
        while (stack.length !== 0) {
            current = stack.shift();
            if (Array.isArray(current)) {
                current.forEach(block => {
                    if (block.getDirection() === BLOCK_DIRECTION.DOWN) {
                        stack.unshift(block);
                    }
                });
            } else{
                var nextBlockList = current.getNextBlockList();
                var isDownBlock = nextBlockList.some(nextBlock => {
                    if (checkBlock && nextBlock.getUUID() === checkBlock.getUUID()) {
                        current = checkBlock.getPrevBlock();
                        // checkBlock.untactBlock();
                        return false;
                    }
                    if (nextBlock.getDirection() === BLOCK_DIRECTION.DOWN) {
                        current = nextBlock;
                        stack.unshift(nextBlock);
                        return true;
                    }
                });
                if ( !isDownBlock ) {
                    break;
                }
            }
        }
        return current;
    }

    /**
     * if 혹은 try 블럭에서 elif 혹은 except 블록을 제거하는 함수
     * @param {if or try BLOCK} that 
     * @param {elif or except BLOCK} elifOrExceptBlock 
     */
    BlockContainer.prototype.deleteElifOrExceptBlock = function(thatBlock, elifOrExceptBlock) {
        var prevBlock = elifOrExceptBlock.getPrevBlock();
        if ( prevBlock ) {
            var nextBlockDataList = prevBlock.getNextBlockList();
            nextBlockDataList.some(( nextBlock, index) => {
                if (nextBlock.getUUID() === elifOrExceptBlock.getUUID()) {
                    nextBlockDataList.splice(index, 1);
                    return true;
                }
            });
        }

        elifOrExceptBlock.setPrevBlock(null);
        elifOrExceptBlock.getNextBlockList().some(block => {
            if (block.getDirection() === BLOCK_DIRECTION.INDENT &&
                elifOrExceptBlock.getFirstIndentBlock().getUUID() !== block.getUUID()) {
                block.untactBlock();
                block.deleteBlock();
                return true;
            }
        });

        elifOrExceptBlock.getFirstIndentBlock().getNextBlockList().forEach(block => {
            block.untactBlock();
            block.deleteBlock();
        });

        elifOrExceptBlock.getHolderBlock().setPrevBlock(null);

        $(elifOrExceptBlock.getBlockMainDom()).remove();
        $(elifOrExceptBlock.getContainerDom()).remove();
        $(elifOrExceptBlock.getFirstIndentBlock().getBlockMainDom()).remove();
        $(elifOrExceptBlock.getFirstIndentBlock().getContainerDom()).remove();
        $(elifOrExceptBlock.getHolderBlock().getBlockMainDom()).remove();
        $(elifOrExceptBlock.getHolderBlock().getContainerDom()).remove();

        elifOrExceptBlock.getHolderBlock().getNextBlockList().some(block => {
            if (block.getDirection() === BLOCK_DIRECTION.DOWN) {
                prevBlock.setNextBlockList([block]);
                block.setPrevBlock(prevBlock);
                return true;
            }
        });
        
        this.renderBlockLeftHolderListHeight();

        this.deleteBlock(elifOrExceptBlock.getUUID());
        this.deleteBlock(elifOrExceptBlock.getFirstIndentBlock().getUUID());
        this.deleteBlock(elifOrExceptBlock.getHolderBlock().getUUID());

        this.renderBlockOptionTab();
        thatBlock.calculateDepthFromRootBlockAndSetDepth();
    }

    /** else block을 생성, 삭제하는 함수를 bind하는 이벤트 함수  
     * @param {if or for or try BLOCK} that 
     * @param {ELSE or FOR_ELSE or FINALLY} blockCodeLineType 
     */
    BlockContainer.prototype.bindElseBlockEvent = function(that, blockCodeLineType) {
        var blockContainerThis = that.getBlockContainerThis();
        // var stateStr = that.getState_IsIfElseOrIsForElseOrIsFinally();
        var stateStr = '';
        if (blockCodeLineType === BLOCK_CODELINE_TYPE.ELSE) {
            stateStr = STATE_isIfElse;
        } else if (blockCodeLineType === BLOCK_CODELINE_TYPE.FOR_ELSE) {
            stateStr = STATE_isForElse;
        } else {
            stateStr = STATE_isFinally;
        }
        var uuid = that.getUUID();

        /** else yes */
        $(`.vp-nodeeditor-else-yes-${uuid}`).click(function() {
            if (that.getState(stateStr) === true) {
                blockContainerThis.renderBlockOptionTab();
                return;
            }

            that.setState({
                [`${stateStr}`]: true
            });
        
            var selectedBlock = that.getLastElifBlock() || that;
            var newBlock = mapTypeToBlock(blockContainerThis, blockCodeLineType, {pointX: 0, pointY: 0});
  
            selectedBlock.getHolderBlock().appendBlock_old(newBlock, BLOCK_DIRECTION.DOWN);
            
            if (blockCodeLineType === BLOCK_CODELINE_TYPE.ELSE) {
                that.ifElseBlock = newBlock;
            } else if (blockCodeLineType === BLOCK_CODELINE_TYPE.FOR_ELSE) {
                that.forElseBlock = newBlock;
                that.setForElseBlock(newBlock);
            } else {
                that.finallyBlock = newBlock;
            }

            newBlock.setParentBlock(that);

            that.calculateDepthFromRootBlockAndSetDepth();

            blockContainerThis.renderBlockOptionTab();   
            blockContainerThis.renderBlockLeftHolderListHeight();
 
            $(`.vp-nodeeditor-else-yes-${uuid}`).css(STR_BORDER, `2px solid yellow`);
            $(`.vp-nodeeditor-else-no-${uuid}`).css(STR_BORDER, `2px solid black`);

            blockContainerThis.reRenderBlockList();
            blockContainerThis.renderBlockLineNumberInfoDom_sortBlockLineAsc();
        });

        /** else no */
        $(`.vp-nodeeditor-else-no-${uuid}`).click(function() {
            blockContainerThis.deleteElseBlockEvent(that, blockCodeLineType);
        });
    }

    /** else block을 삭제하는 메소드 */
    BlockContainer.prototype.deleteElseBlockEvent = function(that, blockCodeLineType) {
        var blockContainerThis = that.getBlockContainerThis();
        var uuid = that.getUUID();

        // var stateStr = that.getState_IsIfElseOrIsForElseOrIsFinally();
        var stateStr = '';
        if (blockCodeLineType === BLOCK_CODELINE_TYPE.ELSE) {
            stateStr = STATE_isIfElse;
        } else if (blockCodeLineType === BLOCK_CODELINE_TYPE.FOR_ELSE) {
            stateStr = STATE_isForElse;
        } else {
            stateStr = STATE_isFinally;
        }

        if (that.getState(stateStr) === false) {  
            blockContainerThis.renderBlockOptionTab();   
            return;
        }

        that.setState({
            [`${stateStr}`]: false
        });

        var elseBlock;
        if (blockCodeLineType === BLOCK_CODELINE_TYPE.ELSE) {
            elseBlock = that.ifElseBlock;
        } else if (blockCodeLineType === BLOCK_CODELINE_TYPE.FOR_ELSE) {
            elseBlock = that.forElseBlock;
        } else {
            elseBlock = that.finallyBlock;
        }

        var prevBlock = elseBlock.getPrevBlock();
        if ( prevBlock ) {
            var nextBlockDataList = prevBlock.getNextBlockList();
            nextBlockDataList.some(( nextBlock, index) => {
                if (nextBlock.getUUID() === elseBlock.getUUID()) {
                    nextBlockDataList.splice(index, 1);
                    return true;
                }
            });
        }

        elseBlock.setPrevBlock(null);
        elseBlock.getNextBlockList().some(block => {
            if (block.getDirection() === BLOCK_DIRECTION.INDENT &&
            elseBlock.getFirstIndentBlock().getUUID() !== block.getUUID()) {
                block.untactBlock();
                block.deleteBlock();
                return true;
            }
        });

        elseBlock.getFirstIndentBlock().getNextBlockList().forEach(block => {
            block.untactBlock();
            block.deleteBlock();
        });

        elseBlock.getHolderBlock().setPrevBlock(null);

        $(elseBlock.getBlockMainDom()).remove();
        $(elseBlock.getContainerDom()).remove();
        $(elseBlock.getFirstIndentBlock().getBlockMainDom()).remove();
        $(elseBlock.getFirstIndentBlock().getContainerDom()).remove();
        $(elseBlock.getHolderBlock().getBlockMainDom()).remove();
        $(elseBlock.getHolderBlock().getContainerDom()).remove();

        elseBlock.getHolderBlock().getNextBlockList().some(block => {
            if (block.getDirection() === BLOCK_DIRECTION.DOWN) {
                prevBlock.setNextBlockList([block]);
                block.setPrevBlock(prevBlock);
                return true;
            }
        });


        blockContainerThis.renderBlockLeftHolderListHeight();

        blockContainerThis.deleteBlock(elseBlock.getUUID());
        blockContainerThis.deleteBlock(elseBlock.getFirstIndentBlock().getUUID());
        blockContainerThis.deleteBlock(elseBlock.getHolderBlock().getUUID());

        blockContainerThis.renderBlockOptionTab();   
        that.calculateDepthFromRootBlockAndSetDepth();

        if (blockCodeLineType === BLOCK_CODELINE_TYPE.ELSE) {
            that.ifElseBlock = null;
        } else if (blockCodeLineType === BLOCK_CODELINE_TYPE.FOR_ELSE) {
            that.forElseBlock = null;
        } else {
            that.finallyBlock = null;
        }

        elseBlock.setParentBlock(null);

        $(`.vp-nodeeditor-else-no-${uuid}`).css(STR_BORDER, `2px solid yellow`);
        $(`.vp-nodeeditor-else-yes-${uuid}`).css(STR_BORDER, `2px solid black`);

        blockContainerThis.reRenderBlockList();
        blockContainerThis.renderBlockLineNumberInfoDom_sortBlockLineAsc();
    }

    /** def 파라미터 변경 이벤트 함수 바인딩 */
    BlockContainer.prototype.bindDefInParamListEvent = function(that, defInParamList) {
        var uuid = that.getUUID();
        var blockContainerThis = this;
        var defInParamList = defInParamList;

        defInParamList.forEach((defInParams, index ) => {
            // const { defParamName, defDefaultVal ,defType } = defInParams;

            /** def 이름 변경 이벤트 함수 바인딩 */
            $(`.vp-nodeeditor-input-def-param-${index}-${uuid}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                renderInputRequiredColor(this);
                var changedParamName = $(this).val();
            
                var updatedData = {
                    defParamName: changedParamName
                    , defDefaultVal : that.getState(STATE_defInParamList)[index].defDefaultVal 
                    , defType: that.getState(STATE_defInParamList)[index].defType
                }
                that.setState({
                    defInParamList:  [ ...that.getState(STATE_defInParamList).slice(0, index), updatedData,
                                       ...that.getState(STATE_defInParamList).slice(index+1, that.getState(STATE_defInParamList).length) ]
                });
                var defInParamStr = generateDefInParamList(that);
                $(`.vp-block-header-param-${that.getUUID()}`).html(defInParamStr);

            });

            /**TODO: 추후 개발 예정 */
            $(`.vp-nodeeditor-input-def-param-${index}-${uuid}`).click(function() {
                // console.log('클릭 def input ', index);
                var dom = $(`<div id="vp_abBoxMenu" 
                                class="vp-nodeeditor-popup" data-type="var" data-idx="7" 
                                style="position: fixed; 
                                left: 1070px; 
                                top: 278px; 
                                display: block;">

                                <div class="vp-nodeeditor-popup-box">
                                    <span class="vp-nodeeditor-popup-menu no-selection" data-menu="load">
                                        <i class="vp-fa fa fa-external-link"></i> 
                                        option page
                                    </span>
                                </div>

                                <div class="vp-nodeeditor-popup-box">
                                    <span class="vp-nodeeditor-popup-menu no-selection" data-menu="run">
                                        <i class="vp-fa fa fa-play"></i> 
                                            run block
                                    </span>
                                </div>

                                <div class="vp-nodeeditor-popup-box">
                                    <span class="vp-nodeeditor-popup-menu no-selection" data-menu="remove">
                                        <i class="vp-fa fa fa-remove"></i> 
                                        remove
                                    </span>
                                </div>
                            </div>`);
                $('body').append(dom);
                $('body').click(function() {
                    $('.vp-nodeeditor-popup').remove();
                });
                // if ( $('body').hasClass('vp-nodeeditor-popup') === true ) {
                //     $('.vp-nodeeditor-popup').remove();
                // }
            });

            /** def default value 변경 이벤트 함수 바인딩 */
            $(`.vp-nodeeditor-input-defaultval-${index}-${uuid}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                var changedDefaultVal = $(this).val();
            
                var updatedData = {
                    defParamName: that.getState(STATE_defInParamList)[index].defParamName
                    , defDefaultVal : changedDefaultVal
                    , defType: that.getState(STATE_defInParamList)[index].defType
                }
                that.setState({
                    defInParamList:  [ ...that.getState(STATE_defInParamList).slice(0, index), updatedData,
                                       ...that.getState(STATE_defInParamList).slice(index+1, that.getState(STATE_defInParamList).length) ]
                });
                var defInParamStr = generateDefInParamList(that);
                $(`.vp-block-header-param-${that.getUUID()}`).html(defInParamStr);

            });

            /** def type select 변경 이벤트 함수 바인딩 */
            $(`.vp-nodeeditor-blockoption-def-type-select-${index}-${uuid}`).change(function()  {
                var defaultParamName = STR_NULL;
                if ( $(STR_COLON_SELECTED, this).val() === '*args' || $(STR_COLON_SELECTED, this).val() === '**kwargs') {
                    defaultParamName = $(STR_COLON_SELECTED, this).val();        
                } 

                var newDefParamName = that.getState(STATE_defInParamList)[index].defParamName;
                if ( newDefParamName === '*args' || newDefParamName === '**kwargs' ) {
                    newDefParamName = STR_NULL; 
                }

                var updatedData = {
                    defParamName: defaultParamName || newDefParamName
                    , defDefaultVal :that.getState(STATE_defInParamList)[index].defDefaultVal 
                    , defType: $(STR_COLON_SELECTED, this).val()
                }
       
                if ($(STR_COLON_SELECTED, this).val() !== 'default') {
                    updatedData.defDefaultVal = STR_NULL;
                }
                
                that.setState({
                    defInParamList:  [ ...that.getState(STATE_defInParamList).slice(0, index), updatedData,
                                       ...that.getState(STATE_defInParamList).slice(index+1, that.getState(STATE_defInParamList).length) ]
                });
                var defInParamStr = generateDefInParamList(that);
                $(`.vp-block-header-param-${that.getUUID()}`).html(defInParamStr);
                blockContainerThis.renderBlockOptionTab();
            });
        });
    }

    /** class, def, return Block의 옵션 파라미터 생성 이벤트 함수 바인딩 */
    BlockContainer.prototype.bindCreateParamEvent = function(block, blockCodeLineType) {
        var blockContainerThis = this;

        $(STR_DOT + VP_CLASS_NODEEDITOR_PARAM_PLUS_BTN + '-' + `${block.getUUID()}`).click(function() {
            var inParamList = STR_NULL;
            var inParamListName = STR_NULL;
            var newData = STR_NULL;

            if ( blockCodeLineType === BLOCK_CODELINE_TYPE.CLASS ) {
                inParamList = block.getState(STATE_classInParamList);
                inParamListName = STATE_classInParamList;
            } else if ( blockCodeLineType === BLOCK_CODELINE_TYPE.DEF ) {
                inParamList = block.getState(STATE_defInParamList);
                inParamListName = STATE_defInParamList;
                newData = {
                    defParamName: `vp_i${inParamList.length}`
                    , defDefaultVal : STR_NULL
                    , defType: STR_NULL
                }
            } else {
                inParamList = block.getState(STATE_returnOutParamList);
                inParamListName = STATE_returnOutParamList;
            }
           
            block.setState({
                [`${inParamListName}`]: [ ...inParamList, newData ]
            });

            if ( blockCodeLineType === BLOCK_CODELINE_TYPE.DEF ) {
                var defInParamStr = generateDefInParamList(block);
                $(`.vp-block-header-param-${block.getUUID()}`).html(defInParamStr);
            }

            blockContainerThis.renderBlockOptionTab(); 
            inParamList.forEach( (_,index) => {
                renderInputRequiredColor( STR_DOT + VP_CLASS_NODEEDITOR_INPUT_PARAM + '-' + `${index}` + '-' + `${block.getUUID()}`);
            });
            renderInputRequiredColor(STR_DOT + VP_CLASS_NODEEDITOR_INPUT_PARAM + '-' + `${inParamList.length}` + '-' + `${block.getUUID()}`);
        });
    }

    /** class, def, return Block의 옵션 파라미터 삭제 이벤트 함수 바인딩 */
    BlockContainer.prototype.bindDeleteParamEvent = function(block, blockCodeLineType) {
        var blockContainerThis = this;
        $(STR_DOT + VP_CLASS_NODEEDITOR_PARAM_DELETE_BTN + '-' + `${block.getUUID()}`).click(function() {
            var inParamList = STR_NULL;
            var inParamListName = STR_NULL;
            if ( blockCodeLineType === BLOCK_CODELINE_TYPE.CLASS ) {
                inParamList = block.getState(STATE_classInParamList);
                inParamListName = STATE_classInParamList;
            } else if ( blockCodeLineType === BLOCK_CODELINE_TYPE.DEF ) {
                inParamList = block.getState(STATE_defInParamList);
                inParamListName = STATE_defInParamList;
            } else {
                inParamList = block.getState(STATE_returnOutParamList);
                inParamListName = STATE_returnOutParamList;
            }

            var index = inParamList.length-1;
            block.setState({
                [`${inParamListName}`]: [ ...inParamList.slice(0, index), 
                                          ...inParamList.slice(index+1, inParamList.length) ]
            });
            // block.renderBottomOption();
            blockContainerThis.renderBlockOptionTab(); 
            var inParamStr = STR_NULL;
            if ( blockCodeLineType === BLOCK_CODELINE_TYPE.CLASS ) {
                inParamStr = generateClassInParamList(block);
            } else if ( blockCodeLineType === BLOCK_CODELINE_TYPE.DEF ) {
                inParamStr = generateDefInParamList(block);
            } else {
                inParamStr = generateReturnOutParamList(block);
            }
            
            $(STR_DOT + VP_CLASS_BLOCK_HEADER_PARAM + '-' + `${block.getUUID()}`).html(inParamStr);
        });
    }

    BlockContainer.prototype.renderBlockOptionTab = function() {
        var that = this;
        var optionTab = $('.vp-nodeeditor-option-tab');

        var blockList = this.getBlockList();
        blockList.some(block => {
            if ( block.getIsSelected() === true) {
                block.renderResetBottomLowerDepthChildsBlockOption();
                block.renderBottomOption();

                var childLowerDepthBlockList = block.getChildLowerDepthBlockList_option();
                if ( childLowerDepthBlockList.length > 0 ) {
                    var blockName = block.getBlockName();
                    var blockNameFirstCharUpper = makeFirstCharToUpperCase(blockName); 
                    var childOptionTab = $(`<div class='vp-nodeeditor-tab-navigation-node-block
                                                        vp-nodeeditor-option-tab-childs-option'>
                                                <div class='vp-nodeeditor-tab-navigation-node-childs-top-option-title'
                                                    style='justify-content: flex-start;'>
                                                    <div class='vp-nodeeditor-panel-area-vertical-btn 
                                                                vp-nodeeditor-arrow-up'>▲</div>
                                                    <span class='vp-block-blocktab-name 
                                                                    vp-block-blocktab-name-title'
                                                            style="font-size: 16px;">${blockNameFirstCharUpper} Child Options</span>
                                                    
                                                </div>

                                                <div class="vp-nodeeditor-bottom-optional-tab-view 
                                                            vp-nodeeditor-scrollbar">

                                                </div>
                                            </div>`);
                    optionTab.append(childOptionTab);
                    /**  블럭 up down 버튼 */
                    that.bindArrowBtnEvent();

                }
                childLowerDepthBlockList.forEach( (block, index) => {
                    block.setIsLowerDepthChild(true);
                    block.renderBottomOption();
                });
                return true;
            }
        });

 
        this.resizeScreen();
    }


    BlockContainer.prototype.generateCode = function(isClicked) {
        var importPackageThis = this.getImportPackageThis();
        importPackageThis.generateCode(true, true, isClicked);
    }

    BlockContainer.prototype.resizeScreen = function() {
        var vpNodeEditorMainRect = $('.vp-nodeeditor-main')[0].getBoundingClientRect();
        var vpNodeEditorLeftRect = $('.vp-nodeeditor-left')[0].getBoundingClientRect();
        var vpNodeEditorRightRect = $('.vp-nodeeditor-right')[0].getBoundingClientRect();

        var vpNodeEditorOptionTabWidth = vpNodeEditorMainRect.width - vpNodeEditorLeftRect.width - vpNodeEditorRightRect.width;
        $('.vp-nodeeditor-option-tab').css('width', vpNodeEditorOptionTabWidth);
        $('.vp-nodeeditor-codeline-ellipsis').css('max-width', vpNodeEditorLeftRect.width - 180 );

    }

    BlockContainer.prototype.bindArrowBtnEvent = function() {
                            /**  블럭 up down 버튼 */
        $(`.vp-nodeeditor-panel-area-vertical-btn`).off();
        $(`.vp-nodeeditor-panel-area-vertical-btn`).click(function() {
            if ($(this).hasClass(`vp-nodeeditor-arrow-down`)) {
                $(this).removeClass(`vp-nodeeditor-arrow-down`);
                $(this).addClass(`vp-nodeeditor-arrow-up`);
                $(this).html(`▲`);
                $(this).parent().parent().removeClass(`vp-nodeeditor-minimize`);
            } else {
                $(this).removeClass(`vp-nodeeditor-arrow-up`);
                $(this).addClass(`vp-nodeeditor-arrow-down`);
                $(this).html(`▼`);
                $(this).parent().parent().addClass(`vp-nodeeditor-minimize`);
            }
        });

    }

    return BlockContainer;
});
