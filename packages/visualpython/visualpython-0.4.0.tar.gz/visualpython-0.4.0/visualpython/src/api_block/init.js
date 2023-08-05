define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'

    , './api.js'    
    , './config.js'
    , './constData.js'
    , './blockContainer.js'
    , './createBlockBtn.js'
], function ( $,vpCommon, vpConst, api, config, constData, blockContainer, createBlockBtn) {
    //FIXME: 추후 소스 전체 리펙토링
    // const { changeOldToNewState
    //     , findStateValue
    //     , mapTypeToName } = api;
    const { PROCESS_MODE } = config;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOCUSED_PAGE_TYPE

            , VP_CLASS_NODEEDITOR_RIGHT
            , VP_CLASS_NODEEDITOR_LEFT
            , VP_CLASS_NODEEDITOR_OPTION_TAB
            , VP_CLASS_MAIN_CONTAINER
            , VP_CLASS_NODEEDITOR_TITLE

            , API_BLOCK_PROCESS_PRODUCTION
            , API_BLOCK_PROCESS_DEVELOPMENT
            , NUM_DELETE_KEY_EVENT_NUMBER
            , STR_IS_SELECTED
            , STR_TOP
            , STR_RIGHT
            , STR_SCROLL
            , STR_MSG_BLOCK_DELETED } = constData;
    const BlockContainer = blockContainer;
    const CreateBlockBtn = createBlockBtn;
    
    var init = function(){
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        var blockContainer = new BlockContainer();
            
        var createBlockBtnArray = Object.values(BLOCK_CODELINE_BTN_TYPE);
        new CreateBlockBtn(blockContainer, BLOCK_CODELINE_BTN_TYPE.CODE);
        createBlockBtnArray.forEach(enumData => {
            if (enumData === BLOCK_CODELINE_BTN_TYPE.API || enumData === BLOCK_CODELINE_BTN_TYPE.CODE) {
                return;
            }
            new CreateBlockBtn(blockContainer, enumData);
        });

        /**  블럭 up down 버튼 */
        blockContainer.bindArrowBtnEvent();
      
        /** 블럭 리셋 버튼 */ 
        var buttonContainer = $(`<label class="vp-nodeeditor-tab-click 
                                               vp-nodeeditor-delete-button-container" 
                                        for="menu-open">
                                    <div class="vp-nodeeditor-delete-button">
                                        <svg viewBox="0 0 22 22">
                                            <circle cx="11" cy="11" r="10"></circle>
                                        </svg>
                                    </div>
                                  </label>`);

        /** 블럭 리셋 버튼이 y: 0부터 얼마나 떨어져있는지 계산 */
        $(VP_CLASS_NODEEDITOR_TITLE).append(buttonContainer);
        blockContainer.setResetBlockListButton(buttonContainer);

        $(VP_CLASS_NODEEDITOR_LEFT).on(STR_SCROLL, function() {
            var scrollValue = $(VP_CLASS_NODEEDITOR_LEFT).scrollTop(); 
            $(buttonContainer).css(STR_TOP,  scrollValue);
        });

        $(buttonContainer).click( 
            function(event) {
                if (PROCESS_MODE === API_BLOCK_PROCESS_DEVELOPMENT) {
                    blockContainer.traverseBlockList();
                    var blockHistoryStack = blockContainer.getBlockHistoryStack();
                    // console.log('blockHistoryStack', blockHistoryStack);
                    var ctrlPressedBlockList = blockContainer.getCtrlPressedBlockList();
                    // console.log('ctrlPressedBlockList', ctrlPressedBlockList);
                    return;
                } 
                
                var rootBlockList = blockContainer.getRootBlockList();
                var rootBlock = rootBlockList[0];
                if (rootBlock) {
                    rootBlock.deleteBlock();
                    rootBlock.renderResetBottomOption();
                    blockContainer.setBlockList([]);
                    blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
                }
            }
        );

        /** block number 재배열 버튼 눌렀을 때 */
        var blockLineSortButton = $(`<div class='vp-nodeeditor-sort-blockline-button'>
                                        <i class='vp-fa fa fa-sort-numeric-asc'></i>
                                    </div>`);
        $(VP_CLASS_NODEEDITOR_TITLE).append(blockLineSortButton);
        $(blockLineSortButton).click(function() {
            blockContainer.renderBlockLineNumberInfoDom_sortBlockLineAsc();
        });
        /** block number 재배열 버튼 화면 고정 */
        $(VP_CLASS_NODEEDITOR_LEFT).on(STR_SCROLL, function() {
            var scrollValue = $(VP_CLASS_NODEEDITOR_LEFT).scrollTop(); 
            $(blockLineSortButton).css(STR_TOP,  scrollValue);
        });

        /** board - option 좌우 resize 스크롤 버튼 화면 고정 */
        $(VP_CLASS_NODEEDITOR_LEFT).on(STR_SCROLL, function() {
            var scrollValue = $(VP_CLASS_NODEEDITOR_LEFT).scrollTop(); 
            $('.vp-nodeeditor-left .ui-resizable-handle').css(STR_TOP,  scrollValue);
        });
        /** delete 키 눌렀을 때 */
        $(document).keyup(function(e) {
            var keycode =  e.keyCode 
                                ? e.keyCode 
                                : e.which;
            if(keycode === NUM_DELETE_KEY_EVENT_NUMBER
                && blockContainer.getFocusedPageType() === FOCUSED_PAGE_TYPE.EDITOR){
          
                   /** block에 ctrl + 클릭이 몇번 되었는지 체크 */
                   var blockList = blockContainer.getBlockList();
                   var numIsCtrlPressed = 0;
                   var isCtrlPressedBlockList = [];
                   blockList.some(block => {
                       if ( block.getIsCtrlPressed() === true) {
                           numIsCtrlPressed++;
                           isCtrlPressedBlockList.push(block);
                       };
                   });
                   
                   /** block에 ctrl + 클릭이 2회 이상 */
                   if ( numIsCtrlPressed > 1 ) {
              
                       isCtrlPressedBlockList.some(block => {
                           if ( block.getPrevBlock() === null ) {
                            //    block.clickBlockDeleteButton();
                                block.deleteBlock();
                                block.renderResetBottomOption();
                                blockContainer.setBlockList([]);
                                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
                               return true;
                           }
                           block.deleteLowerDepthChildBlocks();
                           block.renderResetBottomOption();
                           block.renderResetBottomLowerDepthChildsBlockOption();

                           var blockCodeLineType;
                           var blockList = blockContainer.getBlockList();
                           blockList.some(block => {
                                var isSelected = block.getState(STR_IS_SELECTED);
                                if ( isSelected === true ) {
                                    blockCodeLineType = block.getBlockCodeLineType();
                                    return true;
                                }
                           });

                           if (blockCodeLineType === BLOCK_CODELINE_TYPE.ELSE 
                               || blockCodeLineType=== BLOCK_CODELINE_TYPE.FOR_ELSE
                               || blockCodeLineType=== BLOCK_CODELINE_TYPE.FINALLY) {
                               var parentBlock = block.getParentBlock()
                               blockContainer.deleteElseBlockEvent(parentBlock, blockCodeLineType);
                           }
                   
                           blockContainer.reRenderBlockList();
                   
                           /** root block이 아니어야 block number 오름차순 sort 실행 */
                           if (block.getPrevBlock() !== null) {
                                blockContainer.renderBlockLineNumberInfoDom_sortBlockLineAsc();
                           }
                       });
                   /** block에 ctrl + 클릭이 1회 이상 */
                   } else {
                    //    that.clickBlockDeleteButton(); 
                       var blockList = blockContainer.getBlockList();
                       blockList.some(block => {
                           var isSelected = block.getState(STR_IS_SELECTED);
                           if ( isSelected === true ) {
       
                               block.clickBlockDeleteButton();
                               return true;
                           }
                       });
                   }
            } 
        });

        /** page 포커스 해제 */
        $('#notebook, #header, .cell, .CodeMirror-lines').click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.NULL);
        });
        
        $(VP_CLASS_NODEEDITOR_RIGHT).click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);
        });

        $(VP_CLASS_NODEEDITOR_LEFT).click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
        });

        $(VP_CLASS_NODEEDITOR_LEFT).dblclick(function(e) {
            if ( blockContainer.getIsBlockDoubleClicked() === true ) {
                blockContainer.setIsBlockDoubleClicked(false);
                return;
            }
            blockContainer.generateCode();
        });

        $(VP_CLASS_NODEEDITOR_OPTION_TAB).click(function(e) {
            blockContainer.resizeScreen();
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.OPTION);
        });
     
        /** 만약 API_BLOCK 개발 단계면 디버그 모드 발동 */
        if (PROCESS_MODE === API_BLOCK_PROCESS_DEVELOPMENT) {
            var debugButton = $(`<label class="vp-nodeeditor-tab-click 
                                               vp-nodeeditor-debug-button">
                                    <div>
                                        debug
                                    </div>
                                </label>`);
            $(VP_CLASS_NODEEDITOR_LEFT).append(debugButton);
            $(debugButton).click(function() {

                $('.vp-nodeeditor-tab-navigation-body-1').css('display','none');
                $('.vp-nodeeditor-tab-navigation-body-2').css('display','block');
                
                // for (var i = 1; i < 3; i++) {
                //     (function(j){

                //     })(i)
                // }
                console.log('debug 버튼 클릭');
            });


            var undoButton = $(`<div class="vp-nodeeditor-undo-button">
                                    <i class="vp-fa fa fa-undo vp-block-option-icon"
                                    style="font-size: 20px;"></i>
                                </div>`);
        
            var redoButton = $(`<div class="vp-nodeeditor-repeat-button"
                                    style="margin-left: 10px;">
                                    <i class="vp-fa fa fa-repeat vp-block-option-icon"
                                    style="font-size: 20px;"></i>
                                </div>`);

            $('.vp-nodeeditor-title').append(undoButton);
            $('.vp-nodeeditor-title').append(redoButton);

            /** undo */
            $(undoButton).click(function() {
                console.log('undo');
                var popedBlockStack = blockContainer.popBlockHistoryStackAndGet();
                if (popedBlockStack) {
                    console.log('popedBlockStack', popedBlockStack);
                    blockContainer.reRenderBlockList();
                }
            });
            
            /** redo */
            $(redoButton).click(function() {
                console.log('redo');
            });
        }

        /** API Block에서 input 태그 제어 */
        var controlToggleInput = function() {
            $(`.vp-nodeeditor-body`).on("focus", "input", function() {
                Jupyter.notebook.keyboard_manager.disable();
            });
            $(`.vp-nodeeditor-body`).on("blur", "input", function() {
                Jupyter.notebook.keyboard_manager.enable();
            });
        }

        controlToggleInput();
        return blockContainer;
    }

    return init;
});
