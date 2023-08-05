define([
    'nbextensions/visualpython/src/common/constant'
], function ( vpConstant ) {
    const { VP_CLASS_PREFIX_OLD, VP_CLASS_PREFIX } = vpConstant;

    /** ---------------------------------------- API block에서 쓰이는 ENUM TYPE ------------------------------------------ */
    const BLOCK_CODELINE_BTN_TYPE = {
        CLASS: 1
        , DEF: 2
        , IF: 3
        , FOR: 4
        , WHILE: 5
        , IMPORT: 6
        , API: 7
        , TRY: 8
    
        , RETURN: 9
        , BREAK: 10
        , CONTINUE: 11
        , PASS: 12
        , PROPERTY: 13

        , CODE: 999
    }
    
    const BLOCK_CODELINE_TYPE = {
        CLASS: 1
        , DEF: 2
        , IF: 3
        , FOR: 4
        , WHILE: 5
        , IMPORT: 6
        , API: 7
        , TRY: 8

        , RETURN: 9
        , BREAK: 10
        , CONTINUE: 11
        , PASS: 12
        , PROPERTY: 13

        , RETURN_SUB: 14
        , BREAK_SUB: 15
        , CONTINUE_SUB: 16
        , PASS_SUB: 17
        , PROPERTY_SUB: 18

        , ELIF: 100
        , ELSE: 200
        , FOR_ELSE: 201
        , INIT: 300
        , DEL: 400
        , EXCEPT: 500
        , FINALLY: 600
        , CODE: 999
        
        , HOLDER: 1000
        , NULL: 10000
    }
    
    const BLOCK_DIRECTION  = {
        ROOT: -1
        , DOWN: 1
        , INDENT: 2
        , BOTTOM_DOWN: 3
    }
    
    const BLOCK_TYPE = {
        BLOCK: 1
        , SHADOW_BLOCK: 2
        , MOVE_BLOCK: 3
    }
    
    const MAKE_CHILD_BLOCK = {
        MOVE: 1
        , SHADOW: 2
    }
  
    const IMPORT_BLOCK_TYPE = {
        DEFAULT: 1
        , CUSTOM: 2
    }

    const FOCUSED_PAGE_TYPE = {
        NULL: 1
        , BUTTONS: 2
        , EDITOR: 3
        , OPTION: 4
    }

    const API_BLOCK_PROCESS_PRODUCTION = Symbol();
    const API_BLOCK_PROCESS_DEVELOPMENT = Symbol();

    const DEFAULT_VARIABLE_ARRAY_LIST = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g','h','i','j','k','l','m','n','o','p','q','r',
                                          's','t','u','v','w','x','y','z', 'vp', '_num', 'var' ];
    const IMPORT_LIBRARY_LIST = {
        0: { value: 'numpy', text: 'numpy' }
        , 1: { value: 'pandas', text: 'pandas' }
        , 2: { value: 'matplotlib', text: 'matplotlib' }
        , 3: { value: 'seaborn', text: 'seaborn'}
        , 4: { value: 'os', text: 'os'}
        , 5: { value: 'sys', text: 'sys'}
        , 6: { value: 'time', text: 'time'}
        , 7: { value: 'datetime', text: 'datetime'}
        , 8: { value: 'random', text: 'random'}
        , 9: { value: 'math', text: 'math'}
    }

    /** ---------------------------------------- const Number ------------------------------------------ */
    const NUM_INDENT_DEPTH_PX = 20;
    const NUM_BLOCK_HEIGHT_PX = 24;

    const NUM_MAX_ITERATION = 1000;

    const NUM_NULL = -1;
    const NUM_ZERO = 0;
    const NUM_HUNDREAD = 100;
    const NUM_THOUSAND = 1000;
    const NUM_DELETE_KEY_EVENT_NUMBER = 46;
    const NUM_DEFAULT_POS_X = 50;
    const NUM_DEFAULT_POS_Y = 0;
    const NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT = 42;
    const NUM_BLOCK_BOTTOM_HOLDER_HEIGHT = 10;
    const NUM_BLOCK_MARGIN_TOP_PX = 2.5;
    const NUM_BLOCK_MARGIN_BOTTOM_PX = 2.5;
    const NUM_CODELINE_LEFT_MARGIN_PX = 30;
    const NUM_SHADOWBLOCK_OPACITY = 0.4;
    const NUM_EXCEED_DEPTH = 6;

    /** ---------------------------------------- const String ------------------------------------------ */
    const STR_NULL = '';
    const STR_ONE_SPACE = ' ';
    const STR_ONE_INDENT = '    ';
    const STR_DIV = 'div';
    const STR_BORDER = 'border';
    const STR_TOP = 'top';
    const STR_LEFT = 'left';
    const STR_RIGHT = 'right';
    const STR_PX = 'px';
    const STR_OPACITY = 'opacity';
    const STR_MARGIN_TOP = 'margin-top';
    const STR_MARGIN_LEFT = 'margin-left';
    const STR_BOX_SHADOW = 'box-shadow';
    const STR_DISPLAY = 'display';
    const STR_BACKGROUND_COLOR = 'background-color';
    const STR_WIDTH = 'width';
    const STR_HEIGHT = 'height';
    const STR_INHERIT = 'inherit';
    const STR_YES = 'yes';
    const STR_NO = 'no';
    const STR_DATA_NUM_ID = 'data-num-id';
    const STR_DATA_DEPTH_ID = 'data-depth-id';
    const STR_NONE = 'none';
    const STR_BLOCK = 'block';
    const STR_SELECTED = 'selected';
    const STR_COLON_SELECTED = ':selected';
    const STR_POSITION = 'position';
    const STR_STATIC = 'static';
    const STR_RELATIVE = 'relative';
    const STR_ABSOLUTE = 'absolute';
    const STR_COLOR = 'color';;

    const STR_CLASS = 'class';
    const STR_DEF = 'def';
    const STR_IF = 'if';
    const STR_FOR = 'for';
    const STR_WHILE = 'while';
    const STR_IMPORT = 'import';
    const STR_API = 'api';
    const STR_TRY = 'try';
    const STR_EXCEPT = 'except';
    const STR_RETURN = 'return';
    const STR_BREAK = 'break';
    const STR_CONTINUE = 'continue';
    const STR_PASS = 'pass';
    const STR_CODE = 'code';
    const STR_ELIF = 'elif';
    const STR_PROPERTY = 'property';

    const STR_TITLE = 'title';
    const STR_HIDDEN = 'hidden';
    const STR_AUTO = 'auto';
    const STR_OVERFLOW_X = 'overflow-x';
    const STR_OVERFLOW_Y = 'overflow-y';
    const STR_IS_SELECTED = 'isSelected';
    const STR_SCROLLHEIGHT = 'scrollHeight';
  
    const STR_SCROLL = 'scroll';

    const STR_OPTION = 'Option';

    const STR_ICON_ARROW_UP = `▲`;
    const STR_ICON_ARROW_DOWN = `▼`;

    const STR_DOT = '.';
    const STR_KEYWORD_NEW_LINE = '\n';
    
    /** ---------------------------------------- const CSS class String ------------------------------------------ */
    const VP_ID_PREFIX = '#';
    const VP_ID_DEF = 'header';
    const VP_ID_CONTROL = 'notebook';

    /** ---------------------------------------- const CSS class String ------------------------------------------ */
    // const VP_CLASS_PREFIX = '.';
    
    // const VP_CLASS_PREFIX = "vp-";
    // const VP_CLASS_PREFIX_OLD = ".vp-";
    const VP_BLOCK = `${VP_CLASS_PREFIX_OLD}block`;
    const VP_CLASS_BLOCK_CONTAINER = `${VP_CLASS_PREFIX}block-container`;

    const VP_BLOCK_CLASS_DEF = 'vp-block-class-def';
    const VP_BLOCK_CONTROL = 'vp-block-control';

    const VP_CLASS_BLOCK_NUM_INFO = `${VP_CLASS_PREFIX}block-num-info`;
    const VP_CLASS_NODEEDITOR_MINIMIZE = `${VP_CLASS_PREFIX}nodeeditor-minimize`;
    const VP_CLASS_NODEEDITOR_ARROW_UP = `${VP_CLASS_PREFIX}nodeeditor-arrow-up`;
    const VP_CLASS_NODEEDITOR_ARROW_DOWN = `${VP_CLASS_PREFIX}nodeeditor-arrow-down`;
    const VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED = `${VP_CLASS_PREFIX}nodeeditor-option-input-required`;

    const VP_CLASS_BLOCK_BOTTOM_HOLDER = `${VP_CLASS_PREFIX}block-bottom-holder`;

    const VP_CLASS_BLOCK_SHADOWBLOCK = `${VP_CLASS_PREFIX_OLD}block-shadowblock`;
    const VP_CLASS_BLOCK_OPTION_BTN = `${VP_CLASS_PREFIX_OLD}block-option-btn`;
    const VP_CLASS_BLOCK_DELETE_BTN = `${VP_CLASS_PREFIX_OLD}block-delete-btn`;
    const VP_CLASS_BLOCK_LEFT_HOLDER = `${VP_CLASS_PREFIX_OLD}block-left-holder`;
    const VP_CLASS_BLOCK_DEPTH_INFO = `${VP_CLASS_PREFIX_OLD}block-depth-info`;
    const VP_CLASS_BLOCK_CTRLCLICK_INFO = `${VP_CLASS_PREFIX_OLD}block-ctrlclick-info`;
    const VP_CLASS_NODEEDITOR_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN = `${VP_CLASS_PREFIX_OLD}nodeeditor-tab-navigation-node-option-title span`;
    const VP_CLASS_NODEEDITOR_MAIN = `${VP_CLASS_PREFIX_OLD}nodeeditor-main`;
    const VP_CLASS_NODEEDITOR_LEFT = `${VP_CLASS_PREFIX_OLD}nodeeditor-left`;
    const VP_CLASS_NODEEDITOR_RIGHT = `${VP_CLASS_PREFIX_OLD}nodeeditor-right`;
    const VP_CLASS_NODEEDITOR_OPTION_TAB = `${VP_CLASS_PREFIX_OLD}nodeeditor-option-tab`;
    const VP_CLASS_NODEEDITOR_BOTTOM_TAB_VIEW = `${VP_CLASS_PREFIX_OLD}nodeeditor-bottom-tab-view`;
    const VP_CLASS_NODEEDITOR_BOTTOM_OPTIONAL_TAB_VIEW = `${VP_CLASS_PREFIX_OLD}nodeeditor-bottom-optional-tab-view`;
    const VP_CLASS_NODEEDITOR_SCROLLBAR = `${VP_CLASS_PREFIX_OLD}nodeeditor-scrollbar`;

    const VP_CLASS_BLOCK_HEADER_PARAM = 'vp-block-header-param';
    const VP_CLASS_NODEEDITOR_INPUT_PARAM = 'vp-nodeeditor-input-param';
    const VP_CLASS_NODEEDITOR_PARAM_PLUS_BTN = 'vp-nodeeditor-param-plus-btn';
    const VP_CLASS_NODEEDITOR_PARAM_DELETE_BTN = 'vp-nodeeditor-param-delete-btn';
    const VP_CLASS_MAIN_CONTAINER = '.vp-main-container';
    const VP_CLASS_NODEEDITOR_TITLE = '.vp-nodeeditor-title';
    const VP_CLASS_SELECTED_SHADOWBLOCK = 'selected-shadowblock';

    /** ---------------------------------------- const Message String --------------------------------------------- */
    const STR_MSG_BLOCK_DELETED = 'Block deleted!';
    const STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON = '# Auto-Generated by VisualPython';
    const STR_MSG_BLOCK_DEPTH_MUSH_NOT_EXCEED_6 = 'Block depth must not exceed 6 !!';

    /** ---------------------------------------- const Phrase String --------------------------------------------- */
    const STR_INPUT_YOUR_CODE = 'input your code';
    const STR_CHANGE_KEYUP_PASTE = 'change keyup paste';

    /** ---------------------------------------- const Image Url String ------------------------------------------- */
    const PNG_VP_APIBLOCK_OPTION_ICON = 'vp-apiblock-option-icon.png';
    const PNG_VP_APIBLOCK_DELETE_ICON = 'vp-apiblock-delete-icon.png';

    /** ---------------------------------------- const State Name String ------------------------------------------ */
    const STATE_classInParamList = 'classInParamList';
    const STATE_className = 'className';
    
    const STATE_defName = 'defName';
    const STATE_defInParamList = 'defInParamList';
    
    const STATE_ifCodeLine = 'ifCodeLine';
    const STATE_isIfElse = 'isIfElse';
    const STATE_isForElse = 'isForElse';
    const STATE_ifConditionList = 'ifConditionList';

    const STATE_elifCodeLine = 'elifCodeLine';
    const STATE_elifList = 'elifList';
    
    const STATE_forCodeLine = 'forCodeLine';
    
    const STATE_whileCodeLine = 'whileCodeLine';
    
    const STATE_baseImportList = 'baseImportList';
    const STATE_customImportList = 'customImportList';
    const STATE_isBaseImportPage = 'isBaseImportPage';
    const STATE_exceptList = 'exceptList';
    const STATE_exceptCodeLine = 'exceptCodeLine';
    const STATE_isFinally = 'isFinally';
    
    const STATE_returnOutParamList = 'returnOutParamList';
    
    const STATE_customCodeLine = 'customCodeLine';
    const STATE_breakCodeLine = 'breakCodeLine';
    const STATE_continueCodeLine = 'continueCodeLine';
    const STATE_passCodeLine = 'passCodeLine';
    const STATE_propertyCodeLine = 'propertyCodeLine';

    /** ---------------------------------------- const Color String ------------------------------------------ */
    const COLOR_ORANGE = '#F37704';
    const COLOR_BLOCK_YELLOW = '#FBB500';
    const COLOR_SKY_BLUE = '#3DA5DF';
    const COLOR_YELLOW = 'yellow';
    const COLOR_WHITE = 'white';
    const COLOR_BLOCK_ICON_BTN = '#E85401';
    const COLOR_GRAY_input_your_code = '#d4d4d4';
    const COLOR_FOCUSED_PAGE = '#66BB6A';

    /** ---------------------------------------- const Error String ------------------------------------------ */
    const ERROR_AB0001_REF_NULL_POINTER = '널 포인터 참조 에러';
    const ERROR_AB0002_INFINITE_LOOP = '무한루프 발생';
 
    return {
        BLOCK_CODELINE_BTN_TYPE
        , BLOCK_CODELINE_TYPE
        , BLOCK_DIRECTION
        , BLOCK_TYPE
        , MAKE_CHILD_BLOCK
        , IMPORT_BLOCK_TYPE
        , FOCUSED_PAGE_TYPE

        , NUM_INDENT_DEPTH_PX
        , NUM_BLOCK_HEIGHT_PX
        , NUM_MAX_ITERATION
        
        , NUM_NULL
        , NUM_ZERO
        , NUM_HUNDREAD
        , NUM_THOUSAND
        , NUM_DELETE_KEY_EVENT_NUMBER 
        , NUM_DEFAULT_POS_X
        , NUM_DEFAULT_POS_Y
        , NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT
        , NUM_BLOCK_BOTTOM_HOLDER_HEIGHT
        , NUM_BLOCK_MARGIN_TOP_PX
        , NUM_BLOCK_MARGIN_BOTTOM_PX
        , NUM_CODELINE_LEFT_MARGIN_PX
        , NUM_SHADOWBLOCK_OPACITY
        , NUM_EXCEED_DEPTH

        , STR_TOP
        , STR_LEFT
        , STR_RIGHT
        , STR_DIV
        , STR_BORDER
        , STR_PX
        , STR_OPACITY
        , STR_MARGIN_TOP
        , STR_MARGIN_LEFT
        , STR_BOX_SHADOW
        , STR_DISPLAY
        , STR_BACKGROUND_COLOR
        , STR_WIDTH
        , STR_HEIGHT
        , STR_INHERIT
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
        , STR_NO
        , STR_COLOR
        , STR_IS_SELECTED
        , STR_SCROLLHEIGHT

        , STR_TOP
        , STR_SCROLL

        , STR_CLASS
        , STR_DEF
        , STR_IF
        , STR_FOR
        , STR_WHILE
        , STR_IMPORT
        , STR_API
        , STR_TRY
        , STR_EXCEPT
        , STR_RETURN
        , STR_BREAK
        , STR_CONTINUE
        , STR_PASS
        , STR_CODE
        , STR_ELIF
        , STR_PROPERTY

        , STR_TITLE
        , STR_OVERFLOW_X
        , STR_OVERFLOW_Y
        , STR_HIDDEN
        , STR_AUTO
        , STR_OPTION

        , STR_NULL
        , STR_DOT
        , STR_KEYWORD_NEW_LINE
        , STR_ONE_SPACE
        , STR_ONE_INDENT
        
        , VP_BLOCK
        , VP_BLOCK_CLASS_DEF
        , VP_BLOCK_CONTROL

        , VP_CLASS_BLOCK_CONTAINER
        // , VP_CLASS_BLOCK_NULLBLOCK
        , VP_CLASS_BLOCK_NUM_INFO
        , VP_CLASS_BLOCK_SHADOWBLOCK
        , VP_CLASS_BLOCK_OPTION_BTN
        , VP_CLASS_BLOCK_DELETE_BTN
        , VP_CLASS_BLOCK_DEPTH_INFO
        , VP_CLASS_BLOCK_CTRLCLICK_INFO
        , VP_CLASS_BLOCK_LEFT_HOLDER
        , VP_CLASS_BLOCK_BOTTOM_HOLDER

        , VP_CLASS_NODEEDITOR_OPTION_INPUT_REQUIRED
        , VP_CLASS_NODEEDITOR_MAIN
        , VP_CLASS_NODEEDITOR_LEFT
        , VP_CLASS_NODEEDITOR_RIGHT
        , VP_CLASS_NODEEDITOR_OPTION_TAB
        , VP_CLASS_NODEEDITOR_SCROLLBAR
        , VP_CLASS_NODEEDITOR_BOTTOM_TAB_VIEW
        , VP_CLASS_NODEEDITOR_BOTTOM_OPTIONAL_TAB_VIEW
        , VP_CLASS_NODEEDITOR_MINIMIZE
        , VP_CLASS_NODEEDITOR_ARROW_UP
        , VP_CLASS_NODEEDITOR_ARROW_DOWN
        , VP_CLASS_NODEEDITOR_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN
        , VP_CLASS_SELECTED_SHADOWBLOCK

        , VP_CLASS_BLOCK_HEADER_PARAM
        , VP_CLASS_NODEEDITOR_INPUT_PARAM
        , VP_CLASS_NODEEDITOR_PARAM_PLUS_BTN
        , VP_CLASS_NODEEDITOR_PARAM_DELETE_BTN

        , VP_CLASS_MAIN_CONTAINER
        , VP_CLASS_NODEEDITOR_TITLE
        
        , STR_CHANGE_KEYUP_PASTE
        , STR_INPUT_YOUR_CODE

        , STR_MSG_BLOCK_DELETED
        , STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON
        , STR_MSG_BLOCK_DEPTH_MUSH_NOT_EXCEED_6

        , STR_ICON_ARROW_UP
        , STR_ICON_ARROW_DOWN

        , STATE_classInParamList
        , STATE_className
        , STATE_defName
        , STATE_defInParamList
        , STATE_ifCodeLine
        , STATE_ifConditionList
        , STATE_isIfElse
        , STATE_isForElse
        , STATE_elifCodeLine
        , STATE_elifList
        , STATE_forCodeLine
        , STATE_whileCodeLine
        , STATE_baseImportList
        , STATE_customImportList
        , STATE_isBaseImportPage

        , STATE_exceptList
        , STATE_exceptCodeLine
        , STATE_isFinally
        , STATE_returnOutParamList
        , STATE_customCodeLine
        , STATE_breakCodeLine
        , STATE_continueCodeLine
        , STATE_passCodeLine
        , STATE_propertyCodeLine
        
        , COLOR_ORANGE
        , COLOR_BLOCK_YELLOW
        , COLOR_SKY_BLUE
        , COLOR_YELLOW
        , COLOR_WHITE
        , COLOR_BLOCK_ICON_BTN
        , COLOR_GRAY_input_your_code
        , COLOR_FOCUSED_PAGE

        , IMPORT_LIBRARY_LIST
        , DEFAULT_VARIABLE_ARRAY_LIST

        , PNG_VP_APIBLOCK_OPTION_ICON
        , PNG_VP_APIBLOCK_DELETE_ICON

        , API_BLOCK_PROCESS_PRODUCTION
        , API_BLOCK_PROCESS_DEVELOPMENT

        , ERROR_AB0001_REF_NULL_POINTER
        , ERROR_AB0002_INFINITE_LOOP
    }
});
