define([
    'nbextensions/visualpython/src/common/vpCommon'

    , './api.js'
    , './constData.js'
    , './block.js'
    , './shadowBlock.js'
    , './blockRenderer.js'
], function (vpCommon, api, constData, blockData, shadowBlock, blockRenderer ) {
    const { changeOldToNewState
            , findStateValue
            , mapTypeToName
            , pxStrToNum } = api;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK 
            , FOCUSED_PAGE_TYPE

            , NUM_BLOCK_HEIGHT_PX
            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_ZERO
            , NUM_DEFAULT_POS_X
            , NUM_DEFAULT_POS_Y
            , NUM_BLOCK_MARGIN_TOP_PX
            , NUM_BLOCK_MARGIN_BOTTOM_PX
            , NUM_EXCEED_DEPTH

            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_BORDER
            , STR_PX
            , STR_OPACITY
            , STR_MARGIN_TOP
            , STR_MARGIN_LEFT
            , STR_DISPLAY
            , STR_BACKGROUND_COLOR
            , STR_HEIGHT
            , STR_YES
            , STR_DATA_NUM_ID 
            , STR_DATA_DEPTH_ID
            , STR_NONE
            , STR_BLOCK
            , STR_SELECTED
            , STR_COLON_SELECTED
            , STR_POSITION
            , STR_STATIC
            , STR_RELATIVE
            , STR_ABSOLUTE

            , STR_CLASS
            , STR_DEF
            , STR_IF
            , STR_FOR
            , STR_WHILE
            , STR_IMPORT
            , STR_API
            , STR_TRY
            , STR_RETURN
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_ELIF
            , STR_PROPERTY
            , STR_SCROLLHEIGHT

            , STR_OVERFLOW_X
            , STR_OVERFLOW_Y
            , STR_HIDDEN
            , STR_AUTO
            , VP_CLASS_NODEEDITOR_MAIN

            , VP_CLASS_BLOCK_CONTAINER
            , VP_CLASS_BLOCK_SHADOWBLOCK
            , VP_CLASS_BLOCK_DELETE_BTN
            , VP_CLASS_NODEEDITOR_LEFT
            , VP_CLASS_NODEEDITOR_BOTTOM_TAB_VIEW
            , VP_CLASS_BLOCK_LEFT_HOLDER
            , VP_CLASS_NODEEDITOR_MINIMIZE
            , VP_CLASS_NODEEDITOR_ARROW_UP
            , VP_CLASS_NODEEDITOR_ARROW_DOWN
            , VP_CLASS_NODEEDITOR_SCROLLBAR
            , VP_CLASS_SELECTED_SHADOWBLOCK
            , STR_CHANGE_KEYUP_PASTE

            , STATE_classInParamList
            , STATE_className
            , STATE_defName
            , STATE_defInParamList
            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_elifCodeLine
            , STATE_elifList
            , STATE_forCodeLine
            , STATE_whileCodeLine
            , STATE_baseImportList
            , STATE_customImportList
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_isFinally
            , STATE_returnOutParamList
            , STATE_customCodeLine
            
            , COLOR_ORANGE
            , COLOR_BLOCK_YELLOW
            , COLOR_SKY_BLUE } = constData;  
    const { Block, mapTypeToBlock } = blockData;
    const { renderFocusedPage } = blockRenderer;
    const ShadowBlock = shadowBlock;

    var CreateBlockBtn = function(blockContainerThis, type) { 
        this.blockContainerThis = blockContainerThis;
        this.state = {
            type
            , name: ''
            , isStart: false
            , isDroped: false
        }
        this.rootDomElement = null;

        this.mapTypeToName(type);
        this.render();
        this.bindBtnDragEvent();
    }

    CreateBlockBtn.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }

    CreateBlockBtn.prototype.setIsStart = function(isStart) {
        this.setState({
            isStart
        });
    }
    CreateBlockBtn.prototype.getIsStart = function() {
        return this.state.isStart;
    }
    CreateBlockBtn.prototype.setIsDroped = function(isDroped) {
        this.setState({
            isDroped
        });
    }
    CreateBlockBtn.prototype.getIsDroped  = function() {
        return this.state.isDroped;
    }

    CreateBlockBtn.prototype.getBlockName = function() {
        return this.state.name;
    }

    CreateBlockBtn.prototype.setBlockName = function(name) {
        this.setState({
            name
        });
    }
    CreateBlockBtn.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }

    CreateBlockBtn.prototype.mapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case BLOCK_CODELINE_TYPE.CLASS: {
                name = STR_CLASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.DEF: {
                name = STR_DEF;
                break;
            }
            case BLOCK_CODELINE_TYPE.IF: {
                name = STR_IF;
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR: {
                name = STR_FOR;
                break;
            }
            case BLOCK_CODELINE_TYPE.WHILE: {
                name = STR_WHILE;
                break;
            }
            case BLOCK_CODELINE_TYPE.IMPORT: {
                name = STR_IMPORT;
                break;
            }
            case BLOCK_CODELINE_TYPE.API: {
                name = STR_API;
                break;
            }
            case BLOCK_CODELINE_TYPE.TRY: {
                name = STR_TRY;
                break;
            }
            case BLOCK_CODELINE_TYPE.RETURN: {
                name = STR_RETURN;
                break;
            }
            case BLOCK_CODELINE_TYPE.BREAK: {
                name = STR_BREAK;
                break;
            }
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                name = STR_CONTINUE;
                break;
            }
            case BLOCK_CODELINE_TYPE.PASS: {
                name = STR_PASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                name = STR_PROPERTY;
                break;
            }
            case BLOCK_CODELINE_TYPE.CODE: {
                name = STR_CODE;
                break;
            }

            default: {
                break;
            }
        }

        this.setState({
            name
        });
    }





    CreateBlockBtn.prototype.getBlockMainDom = function() {
        return this.rootDomElement;
    }

    CreateBlockBtn.prototype.setBlockDom = function(rootDomElement) {
        this.rootDomElement = rootDomElement;
    }
    CreateBlockBtn.prototype.getBlockMainDomPosition = function() {
        var rootDom = this.getBlockMainDom();
        var clientRect = $(rootDom)[0].getBoundingClientRect();
        return clientRect;
    }







    // ** Block state 관련 메소드들 */
    CreateBlockBtn.prototype.setState = function(newState) {
            this.state = changeOldToNewState(this.state, newState);
            this.consoleState();
    }
    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    CreateBlockBtn.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }
    CreateBlockBtn.prototype.getStateAll = function() {
        return this.state;
    }
    CreateBlockBtn.prototype.consoleState = function() {
        // console.log(this.state);
    }






    CreateBlockBtn.prototype.render = function() {
        var blockContainer;
        var rootDomElement = $(`<div class='vp-nodeeditor-tab-navigation-node-block-body-btn'>
                                    <span class='vp-block-name'>
                                        ${this.getBlockName()}
                                    </span>
                                </div>`);
        // $(rootDomElement).css('z-index','101');
        this.setBlockDom(rootDomElement);

        var blockCodeType = this.getBlockCodeLineType();
        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS || blockCodeType === BLOCK_CODELINE_TYPE.DEF) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-1-body-inner`);
            $(rootDomElement).addClass('vp-block-class-def');

        } else if (blockCodeType === BLOCK_CODELINE_TYPE.IF || blockCodeType === BLOCK_CODELINE_TYPE.FOR
            || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.TRY
            || blockCodeType === BLOCK_CODELINE_TYPE.ELSE || blockCodeType === BLOCK_CODELINE_TYPE.ELIF
            || blockCodeType === BLOCK_CODELINE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT 
            || blockCodeType === BLOCK_CODELINE_TYPE.FINALLY) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-2-body-inner`);
            $(rootDomElement).addClass('vp-block-control');
  
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.BREAK 
            || blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE 
            || blockCodeType === BLOCK_CODELINE_TYPE.PASS
            || blockCodeType === BLOCK_CODELINE_TYPE.RETURN 
            || blockCodeType === BLOCK_CODELINE_TYPE.PROPERTY
            || blockCodeType === BLOCK_CODELINE_TYPE.CODE
            || blockCodeType === BLOCK_CODELINE_TYPE.IMPORT) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-3-body-inner`);
            $(rootDomElement).css(STR_BACKGROUND_COLOR, COLOR_SKY_BLUE);
        }
        //  else {
        //     blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-3-body-inner`);
        //     $(rootDomElement).css(STR_BACKGROUND_COLOR, COLOR_SKY_BLUE);
     
        // }
  
        blockContainer.append(rootDomElement);
    }

    CreateBlockBtn.prototype.bindBtnDragEvent = function() {
        var that = this;
        var rootDom = this.getBlockMainDom();
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();

        var pos1 = 0;
        var pos2 = 0; 
        var pos3 = 0; 
        var pos4 = 0;
        var buttonX = 0;
        var buttonY = 0;
        var newPointX = 0;
        var newPointY = 0;
        var selectedBlockDirection;
        var shadowBlockList = [];

        // var nodeEditorScrollTop = 0; 
        // var vpDragablebtn = null;
        // var mouseCursor = null;
        $(rootDom).draggable({ 
            addClass: '.vp-dragable-btn',
            appendTo: VP_CLASS_NODEEDITOR_MAIN,
            containment: VP_CLASS_NODEEDITOR_MAIN,
            // appendTo: VP_CLASS_NODEEDITOR_LEFT,
            cursor: 'move', 
            helper: 'clone',
            start: function(event, ui) {
                var rootBlockList = blockContainerThis.getRootBlockList();
               
                rootBlockList.forEach((rootBlock, index) => {
                    var shadowBlock = new ShadowBlock(blockContainerThis, blockCodeLineType, {pointX: 0, pointY: 0}, [],  BLOCK_TYPE.SHADOW_BLOCK);
                    shadowBlock.setRootBlockUUID(rootBlock.getUUID());
                    shadowBlockList.push(shadowBlock);

                    var containerDom = rootBlock.getContainerDom();
                    $(shadowBlock.getBlockMainDom()).css(STR_DISPLAY,STR_NONE);
                    $(shadowBlock.getBlockMainDom()).removeClass(VP_CLASS_SELECTED_SHADOWBLOCK);
                    $(containerDom).append(shadowBlock.getBlockMainDom());
                });
                blockContainerThis.renderBlockLeftHolderListHeight();
            },
            drag: function(event, ui) {  

                /** 현재 drag하는 Block 생성 버튼 위치 구현 */
                blockContainerThis.setEventClientY(event.clientY);
                blockContainerThis.renderBlockLeftHolderListHeight();
                buttonX = event.clientX; 
                buttonY = event.clientY; 

                pos1 = pos3 - buttonX;
                pos2 = pos4 - buttonY;
                pos3 = buttonX;
                pos4 = buttonY;
                var { x: thisX, 
                      y: thisY, 
                      width: thisBlockWidth,
                      height: thisBlockHeight } = that.getBlockMainDomPosition();

                /** 만약  아래 로직에서 + thisBlockWidth + 10이 없다면 마우스 커서 오른쪽으로 이동 됨*/
                newPointX = buttonX - $(VP_CLASS_NODEEDITOR_LEFT).offset().left  + thisBlockWidth + 10 ;
                newPointY = buttonY - $(VP_CLASS_NODEEDITOR_LEFT).offset().top ;

                /** drag Block 생성 버튼 마우스 커서 왼쪽 위로 이동 구현 */
                ui.position = {
                    top: newPointY,
                    left: newPointX
                };

                /** 블록 전체를 돌면서 drag하는 Block 생성 버튼과 Editor위에 생성된 블록들과 충돌 작용  */
                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    /** elif 블럭의 down 방향으로 블럭 생성 금지  */
                    if (block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER
                        && (block.getSupportingBlock().getBlockCodeLineType() === BLOCK_CODELINE_TYPE.ELIF )) {
                        return;
                    }

                    /** if 블럭과 elif, else 블럭의 사이 down 방향으로 블럭 생성 금지  */
                    if (block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER
                        && (block.getSupportingBlock().getBlockCodeLineType() === BLOCK_CODELINE_TYPE.IF)) {
                        var is = block.getNextBlockList().some(nextBlock => {
                            if (nextBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.ELIF 
                                || nextBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.ELSE) {
                                return true;
                            }
                        });
                        if (is === true) {
                            return;
                        }
                    }

                    var { x , y
                          , width: blockWidth
                          , height: blockHeight } = block.getBlockMainDomPosition();
                    var rootBlock = block.getRootBlock();
                    var blockCodeType = block.getBlockCodeLineType();

                    var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight() === 0 
                                                                                        ? blockHeight 
                                                                                        : block.getTempBlockLeftHolderHeight();
           
                    /** 블럭 충돌에서 벗어나는 로직 */
                    if ( (x > buttonX 
                        || buttonX > (x + blockWidth)
                        || y  > buttonY 
                        || buttonY > (y + blockHeight + blockHeight + blockHeight + blockLeftHolderHeight) )
                        // && block.getIsCollision() === true 
                    ) {
                
                        block.renderBlockHolderShadow_2(STR_NONE);
                        block.setIsCollision(false);
                    }

                    /** 블럭 충돌 left holder shadow 생성 로직 */
                    if ( x < buttonX
                        && buttonX < (x + blockWidth )
                        && y  < buttonY
                        && buttonY < (y + blockHeight + blockLeftHolderHeight) ) {     
                  
                        var blockList = blockContainerThis.getBlockList();
      
                        block.renderBlockHolderShadow_2(STR_BLOCK);
                        // var blockDom = block.getBlockMainDom();
                        // if ($(blockDom).hasClass('.vp-block-left-holder')) {
                        //     var rect = $(blockDom).find('.vp-block-left-holder')[0].getBoundingClientRect();
                        //     console.log('rect', rect);
                        // }
    
                    }

                    if ( x < buttonX
                        && buttonX < (x + blockWidth )
                        && y  < buttonY
                        && buttonY < (y + blockHeight  + blockHeight) ) {     
                        // console.log(`${block.getBlockName()}충돌`);
                        var blockList = blockContainerThis.getBlockList();
                        blockList.forEach(block => {
                            block.setIsCollision(false);
                        });
                        block.setIsCollision(true);

                        shadowBlockList.forEach(shadowBlock => {
                            $(shadowBlock.getBlockMainDom()).removeClass(VP_CLASS_SELECTED_SHADOWBLOCK);
                            $(shadowBlock.getBlockMainDom()).css(STR_DISPLAY, STR_NONE);
                            shadowBlock.setSelectBlock(null);
                        });

                        shadowBlockList.some(shadowBlock => {
                            if (shadowBlock.getRootBlockUUID() === rootBlock.getUUID()) {
                                $(shadowBlock.getBlockMainDom()).css(STR_DISPLAY,STR_BLOCK);
                                $(shadowBlock.getBlockMainDom()).addClass(VP_CLASS_SELECTED_SHADOWBLOCK);
                                shadowBlock.setSelectBlock(block);
                                return true;
                            }
                        });

                        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS || blockCodeType === BLOCK_CODELINE_TYPE.DEF || blockCodeType === BLOCK_CODELINE_TYPE.IF ||
                            blockCodeType === BLOCK_CODELINE_TYPE.FOR || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.TRY
                            || blockCodeType === BLOCK_CODELINE_TYPE.ELIF || blockCodeType === BLOCK_CODELINE_TYPE.ELSE
                            || blockCodeType === BLOCK_CODELINE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT || blockCodeType === BLOCK_CODELINE_TYPE.FINALLY) {
                            selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                        } else if (blockCodeType === BLOCK_CODELINE_TYPE.HOLDER) {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        } else {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        }

                        rootBlock.reArrangeChildBlockDomList(block, undefined, selectedBlockDirection);
                    } else {
                        var rootBlockList = blockContainerThis.getRootBlockList();
                        rootBlockList.some(rootBlock => {
                            var containerDom = rootBlock.getContainerDom();
                            var containerDomRect = $(containerDom)[0].getBoundingClientRect();

                            var { x, y, width: containerDomWidth, height: containerDomHeight} = containerDomRect;
                            if ( x < buttonX
                                && buttonX < (x + containerDomWidth)
                                && y  < buttonY
                                && buttonY < (y + containerDomHeight) ) {  
                                // console.log('in colision');
                            } else {
                                shadowBlockList.forEach(shadowBlock => {
                                    $(shadowBlock.getBlockMainDom()).removeClass(VP_CLASS_SELECTED_SHADOWBLOCK);
                                    $(shadowBlock.getBlockMainDom()).css(STR_DISPLAY, STR_NONE);
                                    shadowBlock.setSelectBlock(null);                 
                                });
                                // console.log('not colision');
                            }
                        });
                    }
                });
            },
            stop: function() {
                // console.log('newPointX', newPointX);
                // console.log('newPointY', newPointY);

                var selectedBlock = null;
                var blockList = blockContainerThis.getBlockList();

                var rootBlockList = blockContainerThis.getRootBlockList();
                shadowBlockList.forEach(shadowBlock => {
                    if ( $(shadowBlock.getBlockMainDom ()).hasClass(VP_CLASS_SELECTED_SHADOWBLOCK) ) {
                        selectedBlock = shadowBlock.getSelectBlock();
                    } 
                });

                rootBlockList.forEach(rootBlock => {
                    var rootBlockContainerDom = rootBlock.getContainerDom();
                    $(rootBlockContainerDom).find(VP_CLASS_BLOCK_SHADOWBLOCK).remove();
                });
                var blockList = blockContainerThis.getBlockList();
                if (selectedBlock !== null) {

                    var block = mapTypeToBlock(blockContainerThis, blockCodeLineType , {pointX: 0, pointY: 0});
                    if (blockCodeLineType  === BLOCK_CODELINE_TYPE.CLASS || blockCodeLineType  === BLOCK_CODELINE_TYPE.DEF ) {
                        $(block.getHolderBlock().getBlockMainDom ()).css(STR_BACKGROUND_COLOR,`${COLOR_ORANGE}`);
                    }
                    
                    selectedBlock.appendBlock(block, selectedBlockDirection);

                    block.renderResetColor();
                    block.renderSelectedBlockColor();
           
                    block.selectThisBlock();
                    blockContainerThis.renderBlockOptionTab();
                    block.calculateDepthFromRootBlockAndSetDepth();

                    block.renderEditorScrollTop();

                }  else { 
                    if (blockList.length === 0) {
                        var block = mapTypeToBlock(blockContainerThis, blockCodeLineType , {pointX: 0, pointY: 0});
                        /** ContainerDom 삭제 */
                        {
                            var containerDom = block.getContainerDom();
                            $(containerDom).empty();
                            $(containerDom).remove();
                        }
                        var containerDom = document.createElement(STR_DIV);
                        containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);
                        block.setContainerDom(containerDom);

                        var blockMainDom = block.getBlockMainDom ();
                        $(containerDom).append(blockMainDom);

                        block.setContainerPointX(NUM_DEFAULT_POS_X);
                        block.setContainerPointY(NUM_DEFAULT_POS_Y);
                        $(containerDom).css(STR_TOP,`${NUM_DEFAULT_POS_Y}${STR_PX}`);
                        $(containerDom).css(STR_LEFT,`${NUM_DEFAULT_POS_X}${STR_PX}`);

                        if (blockCodeLineType  === BLOCK_CODELINE_TYPE.CLASS){
                     
                            $(containerDom).append(block.getFirstIndentBlock().getBlockMainDom ());
                            $(containerDom).append(block.getFirstIndentBlock().getFirstIndentBlock().getBlockMainDom ());
                            $(containerDom).append(block.getFirstIndentBlock().getHolderBlock().getBlockMainDom ());
                            
                            if (blockCodeLineType  === BLOCK_CODELINE_TYPE.CLASS || blockCodeLineType  === BLOCK_CODELINE_TYPE.DEF ) {
                                $(block.getHolderBlock().getBlockMainDom ()).css(STR_BACKGROUND_COLOR, COLOR_ORANGE);
                            }
                            $(containerDom).append(block.getHolderBlock().getBlockMainDom ());
                            block.bindDragEvent();
                            block.getFirstIndentBlock().bindDragEvent();
                            block.getFirstIndentBlock().getFirstIndentBlock().bindDragEvent();
                        }

                        if (blockCodeLineType  === BLOCK_CODELINE_TYPE.DEF 
                            || blockCodeLineType  === BLOCK_CODELINE_TYPE.IF || blockCodeLineType  === BLOCK_CODELINE_TYPE.FOR 
                            || blockCodeLineType  === BLOCK_CODELINE_TYPE.WHILE || blockCodeLineType  === BLOCK_CODELINE_TYPE.TRY
                            || blockCodeLineType  === BLOCK_CODELINE_TYPE.FOR_ELSE || blockCodeLineType  === BLOCK_CODELINE_TYPE.EXCEPT 
                            || blockCodeLineType  === BLOCK_CODELINE_TYPE.FINALLY) {

                            $(containerDom).append(block.getFirstIndentBlock().getBlockMainDom ());

                            if (blockCodeLineType  === BLOCK_CODELINE_TYPE.CLASS || blockCodeLineType  === BLOCK_CODELINE_TYPE.DEF ) {
                                $(block.getHolderBlock().getBlockMainDom ()).css(STR_BACKGROUND_COLOR, COLOR_ORANGE);
                            }
                            $(containerDom).append(block.getHolderBlock().getBlockMainDom ());
                            block.bindDragEvent();
                            block.getFirstIndentBlock().bindDragEvent();
                        }

                        $(VP_CLASS_NODEEDITOR_LEFT).append(containerDom);
                        block.renderResetColor();
                        block.renderSelectedBlockColor();
                   
                        block.selectThisBlock();
                        blockContainerThis.renderBlockOptionTab();
                        block.calculateDepthFromRootBlockAndSetDepth();

                        if (blockCodeLineType  === BLOCK_CODELINE_TYPE.CLASS){
                            block.calculateLeftHolderHeightAndSet();
                            block.getFirstIndentBlock().calculateLeftHolderHeightAndSet();
                        } else {
                            block.calculateLeftHolderHeightAndSet();
                        }
                      
                     
                    } else {
                        var rootBlockList = blockContainerThis.getRootBlockList();
                        var rootBlock = rootBlockList[0];

                        var nextBlockList = rootBlock.getNextBlockList();
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
                        
                        // console.log('current', current.getBlockName());
                        var blockCodeType = rootBlock.getBlockCodeLineType();
                        var newBlock = mapTypeToBlock(blockContainerThis, blockCodeLineType , {pointX: 0, pointY: 0});

                        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS || blockCodeType === BLOCK_CODELINE_TYPE.DEF || blockCodeType === BLOCK_CODELINE_TYPE.IF ||
                            blockCodeType === BLOCK_CODELINE_TYPE.FOR || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.TRY ||
                            blockCodeType === BLOCK_CODELINE_TYPE.ELSE || blockCodeType === BLOCK_CODELINE_TYPE.ELIF || blockCodeType === BLOCK_CODELINE_TYPE.FOR_ELSE || 
                            blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT || blockCodeType === BLOCK_CODELINE_TYPE.FINALLY ) {
                            if (current === null) {
                                rootBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                current.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        } else {
                            if (current === null) {
                                rootBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                current.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        }

                        newBlock.renderResetColor();
                        newBlock.renderSelectedBlockColor();
                 
                        newBlock.selectThisBlock();
                        blockContainerThis.renderBlockOptionTab();
                        newBlock.calculateDepthFromRootBlockAndSetDepth();
                        newBlock.calculateLeftHolderHeightAndSet();

                        newBlock.renderEditorScrollTop(true);

                        
                    }
                }

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    var mainDom = block.getBlockMainDom();
                    block.calculateWidthAndSet();
                    $(mainDom).find(VP_CLASS_BLOCK_DELETE_BTN).remove();
                    block.renderBlockHolderShadow(STR_NONE);
                });

                blockContainerThis.renderBlockLeftHolderListHeight();
                // blockContainerThis.mapBlockListDataToBlockJson();

                blockContainerThis.reRenderBlockList();
                blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);
                /** 메모리에 남은 shadowBlockList 삭제 */
                shadowBlockList = [];

                blockContainerThis.renderBlockLineNumberInfoDom_sortBlockLineAsc();

                // blockContainerThis.traverseBlockList();
            }
        });
    }

    return CreateBlockBtn;
});
