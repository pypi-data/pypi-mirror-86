define([
    'nbextensions/visualpython/src/common/constant'

    , './config.js'
    , './constData.js'
], function ( vpConst, config, constData ) {
    const { API_BLOCK_VERSION_v0_1 } = config;
    const { BLOCK_CODELINE_TYPE } = constData;

    var getUUID = function() {
        return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
            (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
        );
    }

    // stateApi
    /** findStateValue 함수
    *  state를 while루프로 돌면서 돌면서 keyName과 일치하는 state의 value값을 찾아 리턴한다
    *  없으면 null을 리턴한다.
    *  @param {object} state 
    *  @param {string} keyName 
    *  @returns {any | null} returnValueOrNull
    */           
    var findStateValue = function(state, keyName) {
        var result = [];
        var stack = [{ context: result
                    , key: 0
                        , value: state }];
        var currContext;
        var returnValueOrNull = null; 
        while (currContext = stack.pop()) {
            var { context, key, value } = currContext;

            if (!value || typeof value != 'object') {
                if (key === keyName) {
                    returnValueOrNull = value;
                    break;
                }
                
                context[key] = value; 
            }
            else if (Array.isArray(value)) {
                if (key === keyName) {
                    returnValueOrNull = value;
                    break;
                }
        
            } else {
                if (key === keyName) {
                    returnValueOrNull = value;
                    break;
                }
                context = context[key] = Object.create(null);
                Object.entries(value).forEach(([ key,value ]) => {
                    stack.push({ context, key, value });
                });
            }
        };
        return returnValueOrNull;
    };

    /** changeOldToNewState 함수
    *  oldState(이전 state 데이터)와 newState(새로운 state 데이터)를 비교해서
        newState로 들어온 새로운 값을 oldState에 덮어 씌운다.
    *  @param {Object} oldState 
    *  @param {Object} newState 
    *  @returns {Object}
    */
    var changeOldToNewState = function(oldState, newState) {
        var result = [];
        var stack = [{ context: result
                        , key: 0
                        , value: oldState }];
        var currContext;
        while (currContext = stack.pop()) {
            var { context, key, value } = currContext;

            if (!value || typeof value != 'object') {
                var newValue = findStateValue(newState, key);
                if ( newValue === "") {
                    context[key] = "";
                }
                else if (newValue === false) {
                    context[key] = false;
                }
                else {
                    context[key] = newValue || value;
                }
            }
            else if (Array.isArray(value)) {
                var newValue = findStateValue(newState, key);
                context[key] = newValue || value;
            } 
            else {
                context = context[key] = Object.create(null);
                Object.entries(value).forEach(([ key, value ]) => {
                    stack.push({context, key, value});
                });
            }
        };
        return result[0];
    };    
    /** createOneArrayValueAndGet
        *  배열의 특정 인덱스 값을 생성하고 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var createOneArrayValueAndGet = function(array, index, newValue) {
        return [ ...array.slice(0, index+1), newValue,
                 ...array.slice(index+1, array.length) ]
    }

    /** updateOneArrayValueAndGet
        *  배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var updateOneArrayValueAndGet = function(array, index, newValue) {
        return [ ...array.slice(0, index), newValue,
                 ...array.slice(index+1, array.length) ]
    }

    /** deleteOneArrayValueAndGet
    *  배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} index 
    *  @returns {Array} New array
    */
    var deleteOneArrayValueAndGet = function(array, index) {
        return [ ...array.slice(0, index), 
                 ...array.slice(index+1, array.length) ]
    }

    /** updateTwoArrayValueAndGet
    *  2차원 배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} row
    *  @param {number} col
    *  @param {number | string} newValue 
    *  @returns {Array} New array
    */
    var updateTwoArrayValueAndGet = function(twoarray, row, col, newValue) {
        var newArray = [...twoarray[row].slice(0, col),newValue,
                        ...twoarray[row].slice(col + 1, twoarray[row].length)]
        return [ ...twoarray.slice(0, row), newArray,
                ...twoarray.slice(row+1, twoarray.length) ]
    }
    /** deleteTwoArrayValueAndGet
    *  2차원 배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} row 
    *  @param {number} col
    *  @returns {Array} New array
    */
    var deleteTwoArrayValueAndGet = function(twoarray, row, col) {
        var newArray = [...twoarray[row].slice(0, col),
                        ...twoarray[row].slice(col + 1, twoarray[row].length)]
        return [ ...twoarray.slice(0, row), newArray,
                ...twoarray.slice(row+1, twoarray.length) ]
    }

    var makeFirstCharToUpperCase = function(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    var mapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case BLOCK_CODELINE_TYPE.CLASS: {
                name = 'class';
                break;
            }
            case BLOCK_CODELINE_TYPE.DEF: {
                name = 'def';
                break;
            }
            case BLOCK_CODELINE_TYPE.IF: {
                name = 'if';
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR: {
                name = 'for';
                break;
            }
            case BLOCK_CODELINE_TYPE.WHILE: {
                name = 'while';
                break;
            }
            case BLOCK_CODELINE_TYPE.IMPORT: {
                name = 'import';
                break;
            }
            case BLOCK_CODELINE_TYPE.API: {
                name = 'api';
                break;
            }
            case BLOCK_CODELINE_TYPE.TRY: {
                name = 'try';
                break;
            }
            case BLOCK_CODELINE_TYPE.RETURN: {
                name = 'return';
                break;
            }
            case BLOCK_CODELINE_TYPE.RETURN_SUB: {
                name = 'return';
                break;
            }
            case BLOCK_CODELINE_TYPE.BREAK: {
                name = 'break';
                break;
            }
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                name = 'continue';
                break;
            }
            case BLOCK_CODELINE_TYPE.PASS: {
                name = 'pass';
                break;
            }
            case BLOCK_CODELINE_TYPE.PASS_SUB: {
                name = 'pass';
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                name = 'property';
                break;
            }
            case BLOCK_CODELINE_TYPE.ELIF: {
                name = 'elif';
                break;
            }
            case BLOCK_CODELINE_TYPE.ELSE: {
                name = 'else';
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR_ELSE: {
                name = 'else';
                break;
            }
            case BLOCK_CODELINE_TYPE.INIT: {
                name = '__init__';
                break;
            }
            case BLOCK_CODELINE_TYPE.DEL: {
                name = '__del__';
                break;
            }
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                name = 'except';
                break;
            }
            case BLOCK_CODELINE_TYPE.FINALLY: {
                name = 'finally';
                break;
            }
            case BLOCK_CODELINE_TYPE.CODE: {
                name = 'code';
                break;
            }
            case BLOCK_CODELINE_TYPE.HOLDER: {
                name = '';
                break;
            }
            default: {
                break;
            }
        }
        return name;
    }

    var removeSomeBlockAndGetBlockList = function(allArray, exceptArray) {
        var lastArray = [];
        allArray.forEach((block) => {
            var is = exceptArray.some((exceptBlock) => {
                if ( block.getUUID() === exceptBlock.getUUID() ) {
                    return true;
                } 
            });

            if (is !== true) {
                lastArray.push(block);
            } 
        });
        return lastArray;
    }
    
    /** if, for 블럭 등에서 여러개 변수 중 특정 랜덤 변수를 선택할 때 사용 */
    var shuffleArray = function(array) {
        const shuffledArray = array
                                .map(a => ([Math.random(),a]))
                                .sort((a,b) => a[0]-b[0])
                                .map(a => a[1]);
        return shuffledArray[0];
    }

    /** API BLOCK 이미지 아이콘 셀렉트 함수 */
    var getImageUrl = function(imageFile) {
        var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'api_block/' + imageFile;
        return url;
    }

    /** 100px string -> 100 number 로 바꾸는 함수
     *  @param {string} pxStr 
     */
    var pxStrToNum = function(pxStr) {
        var index = pxStr.indexOf('p');
        if (index !== -1) {
            var slicedPxStr = pxStr.slice(0,index);
            var slicedPxNum = parseFloat(slicedPxStr);
            return slicedPxNum;
        } else {
            /** 존재하면 안 되는 분기 */
            assertError('실행 중 존재하면 안 되는 분기에 도달했습니다.');
        }
    }
    var generateAPIBlockCode_v0_1 = function() {

    }

    var generateAPIBlockCode = function(apiblockVersion) {
        if (apiblockVersion === API_BLOCK_VERSION_v0_1) {
            generateAPIBlockCode_v0_1();
        }
    }

    /** development -> alert
     *  production -> console.log
     */
    var assertError = function(errorMessage) {
        console.log(errorMessage);
    }
    
    return {
        changeOldToNewState
        , findStateValue

        , createOneArrayValueAndGet
        , updateOneArrayValueAndGet
        , deleteOneArrayValueAndGet

        , makeFirstCharToUpperCase
        , mapTypeToName
        , removeSomeBlockAndGetBlockList

        , shuffleArray

        , getImageUrl

        , pxStrToNum

        , generateAPIBlockCode

        , assertError
    }
});
