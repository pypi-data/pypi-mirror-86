define([
    'nbextensions/visualpython/src/common/vpCommon'
    , './api.js'
    , './constData.js'
], function (vpCommon, api, constData ) {
    const { changeOldToNewState
            , findStateValue
            , mapTypeToName } = api;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK

            , NUM_BLOCK_HEIGHT_PX
            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_ZERO
            , NUM_SHADOWBLOCK_OPACITY
            
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
            , STR_WIDTH

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

            , VP_CLASS_BLOCK_CONTAINER
   
            , VP_CLASS_BLOCK_SHADOWBLOCK
            , VP_CLASS_BLOCK_DELETE_BTN
            , VP_CLASS_NODEEDITOR_LEFT
            , VP_CLASS_NODEEDITOR_BOTTOM_TAB_VIEW
            , VP_CLASS_BLOCK_LEFT_HOLDER
            , VP_CLASS_NODEEDITOR_MINIMIZE
            , VP_CLASS_NODEEDITOR_ARROW_UP
            , VP_CLASS_NODEEDITOR_ARROW_DOWN
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
    
    var ShadowBlock = function(blockContainerThis, type, pointObj, childListDom, blockType, realBlock) {
        this.state = {
            type
            , blockType: BLOCK_TYPE.SHADOW_BLOCK
            , name: ''
            , direction: -1
            , rootBlockUuid: ''
            , pointX: pointObj.pointX 
            , pointY: pointObj.pointY
        }
        this.blockContainerThis = blockContainerThis;

        var name = mapTypeToName(type);
        this.setBlockName(name);
        this.realBlock = realBlock;
        this.rootDom = null;
        this.selectBlock = null;
        this.tempChildListDom = null;
        this.init(childListDom, blockType);
    }

    ShadowBlock.prototype.init = function(childListDom, blockType) {
  
        var childNum = 0;
        var blockRootDom = this.getBlockMainDom();
        $(blockRootDom).remove();
        $(blockRootDom).empty();

        /** root container 생성 */
        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add('vp-block-shadowblock-container');
        $(containerDom).addClass('vp-block-shadowblock');
        $(containerDom).attr('data-num-id', '-1');

        /** root dom 생성 */
        var blockRootDom = document.createElement(STR_DIV);
        blockRootDom.classList.add('vp-block');
        $(blockRootDom).css('width','100%');

        var type = this.getBlockCodeLineType();

        if ( type === BLOCK_CODELINE_TYPE.CLASS || type === BLOCK_CODELINE_TYPE.DEF ||
             type === BLOCK_CODELINE_TYPE.RETURN_SUB ) {
            $(blockRootDom).css(STR_BACKGROUND_COLOR, `${COLOR_ORANGE}`);

        } else if ( type === BLOCK_CODELINE_TYPE.IF || type === BLOCK_CODELINE_TYPE.ELSE 
            || type === BLOCK_CODELINE_TYPE.ELIF || type === BLOCK_CODELINE_TYPE.FOR 
            || type === BLOCK_CODELINE_TYPE.WHILE || type === BLOCK_CODELINE_TYPE.TRY
            || type === BLOCK_CODELINE_TYPE.FOR_ELSE || type === BLOCK_CODELINE_TYPE.EXCEPT 
            || type === BLOCK_CODELINE_TYPE.FINALLY || type === BLOCK_CODELINE_TYPE.PASS_SUB ) {
            $(blockRootDom).css(STR_BACKGROUND_COLOR, `${COLOR_BLOCK_YELLOW}`);

        } else if ( type === BLOCK_CODELINE_TYPE.RETURN || type === BLOCK_CODELINE_TYPE.PROPERTY
                    || type === BLOCK_CODELINE_TYPE.BREAK || type === BLOCK_CODELINE_TYPE.CONTINUE 
                    || type === BLOCK_CODELINE_TYPE.PASS || type === BLOCK_CODELINE_TYPE.IMPORT 
                    || type === BLOCK_CODELINE_TYPE.CODE ) {
            $(blockRootDom).css(STR_BACKGROUND_COLOR, `${COLOR_SKY_BLUE}`);
        }

        
        $(blockRootDom).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);
        $(blockRootDom).css(STR_POSITION, STR_RELATIVE);

        blockRootDom.style.top = `${this.getPointY()}` + STR_PX;
        blockRootDom.style.left = `${this.getPointX()}` + STR_PX;

        var blockInnerDom = $(`<div class='vp-block-inner'></div>`);
        var nameDom = $(`<div class='vp-block-header'>
                            <strong class="vp-nodeeditor-style-flex-column-center 
                                    ${this.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER ? 'vp-block-name' : ''}" 
                                style="margin-right:10px; font-size:12px; color: #252525;">
                                ${this.getBlockName()}
                            </strong>    
                        </div>`);

        $(blockInnerDom).append(nameDom); 
        $(blockRootDom).append(blockInnerDom);

        var rootBlockDepth = 0;
        var childLowerDepthBlockList;
        if (blockType === BLOCK_TYPE.BLOCK) {
            // rootBlockDepth = this.realBlock.getDepth();
            rootBlockDepth = parseInt( $(this.realBlock.getBlockMainDom()).attr(STR_DATA_DEPTH_ID) );

            childLowerDepthBlockList = this.realBlock.getChildLowerDepthBlockList();

            if (type === BLOCK_CODELINE_TYPE.CLASS || type === BLOCK_CODELINE_TYPE.DEF) {
            
                var blockLeftHolder = $('<div class="vp-block-left-holder"></div>');
                var blockLeftHolderHeight = this.realBlock.getTempBlockLeftHolderHeight();
                blockLeftHolder.css(STR_HEIGHT,`${blockLeftHolderHeight}px`);
                $(blockLeftHolder).css(STR_BACKGROUND_COLOR,`${COLOR_ORANGE}`);
                $(blockLeftHolder).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);
          
                this.realBlock.setBlockLeftHolderDom(blockLeftHolder);
                $(blockRootDom).append(blockLeftHolder);
        
            } else if (type === BLOCK_CODELINE_TYPE.IF || type === BLOCK_CODELINE_TYPE.ELSE 
                    || type === BLOCK_CODELINE_TYPE.ELIF || type === BLOCK_CODELINE_TYPE.FOR 
                    || type === BLOCK_CODELINE_TYPE.WHILE || type === BLOCK_CODELINE_TYPE.TRY
                    || type === BLOCK_CODELINE_TYPE.FOR_ELSE || type === BLOCK_CODELINE_TYPE.EXCEPT 
                    || type === BLOCK_CODELINE_TYPE.FINALLY
                    ) {
                        
                var blockLeftHolder = $('<div class="vp-block-left-holder"></div>');
                var blockLeftHolderHeight = this.realBlock.getTempBlockLeftHolderHeight();
                blockLeftHolder.css(STR_HEIGHT,`${blockLeftHolderHeight}px`);
                $(blockLeftHolder).css(STR_BACKGROUND_COLOR,`${COLOR_BLOCK_YELLOW}`);
                $(blockLeftHolder).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);
            
                this.realBlock.setBlockLeftHolderDom(blockLeftHolder);
                $(blockRootDom).append(blockLeftHolder);
    
            } else {

            }
        }

        $(containerDom).append(blockRootDom);
        childNum++;

  
        childListDom.forEach( (childDom,index) => {
            $(childDom).css(STR_OPACITY, NUM_SHADOWBLOCK_OPACITY);
            // var childBlockDepth = childLowerDepthBlockList[index+1].getDepth();
            var childBlockDepth = parseInt( $(childLowerDepthBlockList[index+1].getBlockMainDom()).attr(STR_DATA_DEPTH_ID) );
            var minusedChildBlockDepth = childBlockDepth - rootBlockDepth;

            if (minusedChildBlockDepth <= 0) {
                $(childDom).css('width', '100%');
            } else {
                $(childDom).css('width',`calc(100% - ${NUM_INDENT_DEPTH_PX * minusedChildBlockDepth}px)`);
            }

            $(containerDom).append(childDom);
            childNum++;
        });
        
        this.setBlockDom(containerDom);
    }

    ShadowBlock.prototype.render = function() {
        var blockRootDom = this.getBlockMainDom();
        $('.vp-nodeeditor-left').append(blockRootDom);
    }

    ShadowBlock.prototype.setPointX = function(pointX) {
        this.setState({
            pointX
        });
    }
    ShadowBlock.prototype.setPointY = function(pointY) {
        this.setState({
            pointY
        });
    }
    ShadowBlock.prototype.getPointX = function() {
        return this.state.pointX;
    }
    ShadowBlock.prototype.getPointY = function() {
        return this.state.pointY;
    }
    ShadowBlock.prototype.getBlockName = function() {
        return this.state.name;
    }
    ShadowBlock.prototype.setBlockName = function(name) {
        this.setState({
            name
        });
    }
    ShadowBlock.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }
    ShadowBlock.prototype.setType = function(type) {
        this.setState({
            type
        });
    }
    ShadowBlock.prototype.getBlockType = function() {
        return this.state.blockType;
    }
    ShadowBlock.prototype.setBlockType = function(blockType) {
        this.setState({
            blockType
        });
    }

    ShadowBlock.prototype.setRootBlockUUID = function(rootBlockUuid) {
        this.setState({
            rootBlockUuid
        });
    }
    ShadowBlock.prototype.getRootBlockUUID = function() {
        return this.state.rootBlockUuid;
    }

    ShadowBlock.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }

    ShadowBlock.prototype.getDirection = function() {
        return this.state.direction;
    }
    ShadowBlock.prototype.setDirection = function(direction) {
        this.setState({
            direction
        });
    }








    ShadowBlock.prototype.getBlockMainDom = function() {
        return this.rootDom;
    }
    ShadowBlock.prototype.setBlockDom = function(rootDom) {
        this.rootDom = rootDom;
    }
    ShadowBlock.prototype.getTempChildListDom = function() {
        return this.tempChildListDom;
    }
    ShadowBlock.prototype.setTempChildListDom = function(tempChildListDom) {
        this.tempChildListDom = tempChildListDom;
    }






    ShadowBlock.prototype.setSelectBlock = function(selectBlock) {
        this.selectBlock = selectBlock;
    }
    ShadowBlock.prototype.getSelectBlock = function() {
        return this.selectBlock;
    }
    ShadowBlock.prototype.deleteShadowBlock = function() {
        var blockRootDom = this.getBlockMainDom();
        $(blockRootDom).remove();
        $(blockRootDom).empty();
    }







        // ** Block state 관련 메소드들 */
    ShadowBlock.prototype.setState = function(newState) {
        this.state = changeOldToNewState(this.state, newState);
        this.consoleState();
    }

    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    ShadowBlock.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }
    ShadowBlock.prototype.getStateAll = function() {
        return this.state;
    }
    ShadowBlock.prototype.consoleState = function() {
        // console.log(this.state);
    }

    return ShadowBlock;
});
