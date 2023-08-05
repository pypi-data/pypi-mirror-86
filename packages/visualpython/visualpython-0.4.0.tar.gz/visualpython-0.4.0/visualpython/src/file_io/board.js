define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
    , 'nbextensions/visualpython/src/common/vpBoard'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, libPandas, pdGen, VpBoard) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Board"
        , funcID : "pd_board"
        , libID : "pd000"
    }

    var vpBoard;

    //////////////// FIXME: move to constants file: Data Types constant ///////////////////////

    var _DATA_TYPES_OF_INDEX = [
        // Index 하위 유형
        'RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'
    ]

    var _DATA_TYPES_OF_GROUPBY = [
        // GroupBy 하위 유형
        'DataFrameGroupBy', 'SeriesGroupBy'
    ]

    var _SEARCHABLE_DATA_TYPES = [
        // pandas 객체
        'DataFrame', 'Series', 'Index', 'Period', 'GroupBy', 'Timestamp'
        , ..._DATA_TYPES_OF_INDEX
        , ..._DATA_TYPES_OF_GROUPBY
        // Plot 관련 유형
        //, 'Figure', 'AxesSubplot'
        // Numpy
        //, 'ndarray'
        // Python 변수
        //, 'str', 'int', 'float', 'bool', 'dict', 'list', 'tuple'
    ];

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback, meta) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM))).find(vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE)).addClass(uuid);

            // 옵션 객체 생성
            var varPackage = new VariablePackage(uuid);
            varPackage.metadata = meta;

            // 옵션 속성 할당.
            varPackage.setOptionProp(funcOptProp);
            // html 설정.
            varPackage.initHtml();
            callback(varPackage);  // 공통 객체를 callback 인자로 전달

            vpBoard = new VpBoard(varPackage);
            vpBoard.load();
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "file_io/board.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var VariablePackage = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.package = {
            input: [
                { name: 'vp_varList' },
                { name: 'vp_colList' },
                { name: 'vp_idxList' },
                { name: 'vp_varApiSearch' },
                { name: 'vp_varApiFuncId' }
            ]
        }

        // api list for variable
        // FIXME:
        this.apiList = {
            DataFrame: [
                { name: 'pandas.DataFrame.index', code: 'index' },
                { name: 'pandas.DataFrame.columns', code: 'columns' },
                { name: 'pandas.DataFrame.dtypes', code: 'dtypes' },
                { name: 'pandas.DataFrame.select_dtypes', code: 'select_dtypes()' },
                { name: 'pandas.DataFrame.values', code: 'values' },
                { name: 'pandas.DataFrame.shape', code: 'shape' },
                { name: 'pandas.DataFrame.head', code: 'head()' },
                { name: 'pandas.DataFrame.loc[]', code: 'loc[]' },
                { name: 'pandas.DataFrame.iloc[]', code: 'iloc[]' },
                { name: 'pandas.DataFrame.items', code: 'items()' },
                { name: 'pandas.DataFrame.keys', code: 'keys()' },
                { name: 'pandas.DataFrame.tail', code: 'tail()' },
                { name: 'pandas.DataFrame.where', code: 'where()' },
                { name: 'pandas.DataFrame.add', code: 'add()' },
                { name: 'pandas.DataFrame.sub', code: 'sub()' },
                { name: 'pandas.DataFrame.mul', code: 'mul()' },
                { name: 'pandas.DataFrame.div', code: 'div()' },
                { name: 'pandas.DataFrame.all', code: 'all()' },
                { name: 'pandas.DataFrame.any', code: 'any()' },
                { name: 'pandas.DataFrame.count', code: 'count()' },
                { name: 'pandas.DataFrame.describe', code: 'describe()' },
                { name: 'pandas.DataFrame.max', code: 'max()' },
                { name: 'pandas.DataFrame.mean', code: 'mean()' },
                { name: 'pandas.DataFrame.min', code: 'min()' },
                { name: 'pandas.DataFrame.sum', code: 'sum()' },
                { name: 'pandas.DataFrame.std', code: 'std()' },
                { name: 'pandas.DataFrame.drop', code: 'drop()' },
                { name: 'pandas.DataFrame.drop_duplicates', code: 'drop_duplicates()' },
                { name: 'pandas.DataFrame.dropna', code: 'dropna()' },
                { name: 'pandas.DataFrame.fillna', code: 'fillna()' },
                { name: 'pandas.DataFrame.isna', code: 'isna()' },
                { name: 'pandas.DataFrame.isnull', code: 'isnull()' },
                { name: 'pandas.DataFrame.notna', code: 'notna()' },
                { name: 'pandas.DataFrame.notnull', code: 'notnull()' },
                { name: 'pandas.DataFrame.replace', code: 'replace()' },
                { name: 'pandas.DataFrame.T', code: 'T' }
            ],
            Series: [
                { name: 'pandas.Series.index', code: 'index' },
                { name: 'pandas.Series.array', code: 'array' },
                { name: 'pandas.Series.values', code: 'values' },
                { name: 'pandas.Series.dtype', code: 'dtype' },
                { name: 'pandas.Series.shape', code: 'shape()' },
                { name: 'pandas.Series.size', code: 'size()' },
                { name: 'pandas.Series.T', code: 'T' },
                { name: 'pandas.Series.unique', code: 'unique()' },
                { name: 'pandas.Series.value_counts', code: 'value_counts()' },
                { name: 'pandas.Series.hasnans', code: 'hasnans' },
                { name: 'pandas.Series.dtypes', code: 'dtypes' },
                { name: 'pandas.Series.loc[]', code: 'loc[]' },
                { name: 'pandas.Series.iloc[]', code: 'iloc[]' },
                { name: 'pandas.Series.items', code: 'items()' },
                { name: 'pandas.Series.keys', code: 'keys()' },
                { name: 'pandas.Series.add', code: 'add()' },
                { name: 'pandas.Series.sub', code: 'sub()' },
                { name: 'pandas.Series.mul', code: 'mul()' },
                { name: 'pandas.Series.div', code: 'div()' },
                { name: 'pandas.Series.all', code: 'all()' },
                { name: 'pandas.Series.any', code: 'any()' },
                { name: 'pandas.Series.count', code: 'count()' },
                { name: 'pandas.Series.describe', code: 'describe()' },
                { name: 'pandas.Series.max', code: 'max()' },
                { name: 'pandas.Series.mean', code: 'mean()' },
                { name: 'pandas.Series.min', code: 'min()' },
                { name: 'pandas.Series.sum', code: 'sum()' },
                { name: 'pandas.Series.std', code: 'std()' },
                { name: 'pandas.Series.drop', code: 'drop()' },
                { name: 'pandas.Series.drop_duplicates', code: 'drop_duplicates()' },
                { name: 'pandas.Series.dropna', code: 'dropna()' },
                { name: 'pandas.Series.fillna', code: 'fillna()' },
                { name: 'pandas.Series.isna', code: 'isna()' },
                { name: 'pandas.Series.isnull', code: 'isnull()' },
                { name: 'pandas.Series.notna', code: 'notna()' },
                { name: 'pandas.Series.notnull', code: 'notnull()' },
                { name: 'pandas.Series.replace', code: 'replace()' },
                { name: 'pandas.Series.map', code: 'map(lambda p: p)' }
            ]
        }
    }



    /**
     * vpFuncJS 에서 상속
     */
    VariablePackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    VariablePackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }


    /**
     * html 내부 binding 처리
     */
    VariablePackage.prototype.initHtml = function() {
        var that = this;

        this.showFunctionTitle();

        this.loadVariables();

        $(this.wrapSelector('.vp-oper-connect')).hide();
        $(this.wrapSelector('.vp-del-col')).hide();

        // 변수이름 클릭 시
        $(this.wrapSelector('#vp_varList')).change(function() {
            that.handleVariableSelection();
        });

        // load variables on refresh
        $(this.wrapSelector('#vp_varRefresh')).click(function(event) {
            event.stopPropagation();
            $(that.wrapSelector('#vp_varApiSearch')).autocomplete('option', 'source', []);

            that.loadVariables();
        });

        // column selection
        $(document).on('click', this.wrapSelector('.vp-col-list'), function() {
            that.replaceBoard();
        });
        // operator selection
        $(document).on('click', this.wrapSelector('.vp-oper-list'), function() {
            that.replaceBoard();
        });
        // condition change
        $(document).on('change', this.wrapSelector('.vp-condition'), function() {
            that.replaceBoard();
        });
        // connector selection
        $(document).on('click', this.wrapSelector('.vp-oper-connect'), function() {
            that.replaceBoard();
        });
        // api list change
        $(this.wrapSelector('#vp_varApiSearch')).change(function() {
            that.replaceBoard();
        });

        // on column add
        $(this.wrapSelector('#vp_addCol')).click(function() {
            var clone = $(that.wrapSelector('#vp_colList tr:first')).clone();

            clone.find('input').val('');
            // hide last connect operator
            clone.find('.vp-oper-connect').hide();
            // show connect operator right before last one
            $(that.wrapSelector('#vp_colList .vp-oper-connect:last')).show();
            clone.insertBefore('#vp_colList tr:last');

            // show delete button
            $(that.wrapSelector('#vp_colList tr td .vp-del-col')).show();
        });
        // on column delete
        $(document).on("click", this.wrapSelector('.vp-del-col'), function(event) {
            event.stopPropagation();
            $(this).parent().parent().remove();
            $(that.wrapSelector('#vp_colList .vp-oper-connect:last')).hide();

            var colList = $(that.wrapSelector('#vp_colList tr td:not(:last)'));
            if (colList.length <= 1) {
                colList.find('.vp-del-col').hide();
            }

            that.replaceBoard();
        });

        // on return type change
        $(this.wrapSelector('#vp_returnType')).change(function() {
            // load API List for selected variable
            that.loadApiList();
        });

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/board.css");
    }

    var convertToStr = function(code) {
        if (!$.isNumeric(code)) {
            code = `'${code}'`;
        }
        return code;
    }

    /**
     * make block to add on API Board
     */
    VariablePackage.prototype.makeBlock = function() {
        var varName = $(this.wrapSelector('#vp_varList')).find(':selected').attr('data-var-name');
        if (varName == undefined || varName == '') {
            return [];
        }

        var varType = $(this.wrapSelector('#vp_varList')).find(':selected').attr('data-var-type');

        var returnType = $(this.wrapSelector('#vp_returnType')).val();
        var apiCode = $(this.wrapSelector('#vp_varApiSearch')).val();

        // TODO: add block to board with condition
        // - type: var / type: api(if apiCode is not undefined)
        // - with col/idx or not
        // - api                = df.api
        // - col + api          = df[[col]].api
        // - col                = df[col]
        // - col + dataframe    = df[[col]] //FIXME:
        // - idx                = df.iloc[idx] / df.loc[idx]

        // vpBoard add
        var blocks = [
            { code: varName, type: 'var', next: -1 }
        ];

        // columns + condition block
        var colList = $(this.wrapSelector('#vp_colList tr td:not(:last)'));
        
        var colSelector = [];
        var condSelector = [];
        for (var i = 0; i < colList.length; i++) {
            var colTag = $(colList[i]);
            var colName = colTag.find('.vp-col-list').val();
            var oper = colTag.find('.vp-oper-list').val();
            var cond = colTag.find('.vp-condition').val();
            var connector = i > 0? $(colList[i- 1]).find('.vp-oper-connect').val() : undefined;

            if (colName == "") continue;

            if (oper == '') {
                if (condSelector.length > 0) {
                    var idx = blocks.length;
                    blocks = blocks.concat(condSelector);
                    var lastIdx = blocks.length - 1;
                    // TODO: [] 추가
                    blocks.push({
                        code: '[]', type: 'brac', child: lastIdx
                    });

                    // TODO: idx 연결
                    blocks[idx - 1]['next'] = blocks.length - 1;

                    condSelector = [];
                }
                // column selector
                colSelector.push(colName);
            } else {
                // TODO: 조건식도 호환되도록 해야함
                // condition selector
                if (colSelector.length > 0) {
                    var idx = blocks.length;
                    blocks[idx - 1]['next'] = idx + 2;
                    blocks.push({
                        code: colSelector.map(v => convertToStr(v)).toString(),
                        type: 'code'
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx + 1
                    });
                    
                    colSelector = [];
                }
                var idx = blocks.length + condSelector.length;
                var hasPrev = condSelector.length > 0;
                condSelector = condSelector.concat([
                    { code: varName, type: 'var', next: idx + 2 },     // idx
                    { code: convertToStr(colName), type: 'code' },    
                    { code: '[]', type: 'brac', child: idx + 1 }
                ]);
                if (cond != undefined && cond !== '') {
                    condSelector.push({ code: cond, type: 'code' });
                    condSelector.push({ code: oper, type: 'oper', left: idx, right: idx + 3 });
                } else {
                    condSelector.push({ code: oper, type: 'oper', left: idx, right: -1 });
                }
                if (connector != undefined && hasPrev) {
                    condSelector.push({
                        code: connector, type: 'oper'
                        , left: idx - 1
                        , right: blocks.length + condSelector.length - 1
                    });
                }
            }
        }

        if (colSelector.length > 0) {
            var idx = blocks.length;
            blocks[idx - 1]['next'] = idx + 2;
            blocks.push({
                code: colSelector.map(v => convertToStr(v)).toString(),
                type: 'code'
            });
            blocks.push({
                code: '[]', type: 'brac', child: idx
            });
            blocks.push({
                code: '[]', type: 'brac', child: idx + 1
            });
        }
        if (condSelector.length > 0) {
            var idx = blocks.length;
            blocks = blocks.concat(condSelector);
            var lastIdx = blocks.length - 1;
            // TODO: [] 추가
            blocks.push({
                code: '[]', type: 'brac', child: lastIdx
            });

            // TODO: idx 연결
            blocks[idx - 1]['next'] = blocks.length - 1;

            condSelector = [];
        }

        // api list attach
        // TODO: API 리스트도 returnType에 맞춰서 연결
        if (apiCode != undefined && apiCode != '') {
            blocks[blocks.length -1]['next'] = blocks.length;
            blocks.push({
                code: '.' + apiCode, type: 'api'
            })
        }

        console.log(blocks);

        return blocks;
    }

    /**
     * initialize options
     */
    VariablePackage.prototype.initOptions = function() {
        // init before loadVariable
        // initialize tags
        // $(this.wrapSelector('#vp_varList')).html('');

        // // init before bind selection event
        // // initialize : hide options
        // $(this.wrapSelector('#vp_colList')).closest('tr').hide();
        // $(this.wrapSelector('#vp_idxList')).closest('tr').hide();

        // // init api list
        // $(this.wrapSelector('#vp_varApiList')).html('<ul class="vp-var-api-list"></ul>');

        var that = this;

        // show api list
        $(this.wrapSelector('#vp_varApiSearch')).autocomplete({
            source: {},
            minLength: 2,
            autoFocus: true,
            select: function(event, ui) {
                $(that.wrapSelector('#vp_varApiSearch')).val(ui.item.value);
                $(that.wrapSelector('#vp_varApiFuncId')).val(ui.item.id);

                that.replaceBoard();
            },
            change: function(event, ui) {
                that.replaceBoard();
            }
        });

        $(this.wrapSelector('#vp_varApiSearch')).val('');
        $(this.wrapSelector('#vp_varApiFuncId')).val('');

        // bind event for variable selection
        this.handleVariableSelection();
        // load API List for selected variable
        this.loadApiList();
        
    }

    /**
     * 선택한 패키지명 입력
     */
    VariablePackage.prototype.showFunctionTitle = function() {
        $(this.wrapSelector('.vp_functionName')).text(funcOptProp.funcName);
    }

    /**
     * Variables 조회
     */
    VariablePackage.prototype.loadVariables = function() {
        var that = this;

        // 조회가능한 변수 data type 정의 FIXME: 조회 필요한 변수 유형 추가
        var types = _SEARCHABLE_DATA_TYPES;

        var tagVarList = this.wrapSelector('#vp_varList');
        $(tagVarList).html('');
        
        // HTML 구성
        pdGen.vp_searchVarList(types, function(result) {
            var jsonVars = result.replace(/'/gi, `"`);
            var varList = JSON.parse(jsonVars);

            // 변수목록 추가
            varList.forEach(varObj => {
                if (types.includes(varObj.varType) && varObj.varName[0] !== '_') {
                    var tagOption = document.createElement('option');
                    $(tagOption).attr({
                        'data-var-name': varObj.varName,
                        'data-var-type': varObj.varType,
                        'value': varObj.varName
                    });
                    tagOption.innerText = `${varObj.varName} (${varObj.varType})`;

                    $(tagVarList).append(tagOption);
                }
            });

            that.initOptions();

        });
    };

    VariablePackage.prototype.replaceBoard = function() {
        // clear board
        vpBoard.clear();
        // add block
        vpBoard.addBlocks(this.makeBlock());
    }

    /**
     * Bind variable selection events
     * - on change variables
     */
    VariablePackage.prototype.handleVariableSelection = function() {
        // get selected variable info
        var varName = $(this.wrapSelector('#vp_varList')).find(':selected').data('var-name');
        var varType = $(this.wrapSelector('#vp_varList')).find(':selected').data('var-type');

        // initialize on event : hide options
        $(this.wrapSelector('#vp_colList')).closest('tr').hide();

        // Pandas Objects
        // if pandas object
        if (varType == 'DataFrame') {
            // 2. DataFrame - show index, columns
            this.getObjectDetail(varName, 'columns', '.vp-col-list');

            $(this.wrapSelector('#vp_colList')).closest('tr').show();
        } else {
            // series
            // replace board with now status of board option
            this.replaceBoard();
        }

        // set return type
        $(this.wrapSelector('#vp_returnType')).val(varType);
        // load API List for selected variable
        this.loadApiList();

        
    };

    /**
     * Get variable detail
     * @param {string} varName 
     * @param {string} property 
     * @param {string} selectId select tag id with selector
     */
    VariablePackage.prototype.getObjectDetail = function(varName, property, selectId) {
        var that = this;
        // 변수 col, idx 정보 조회 command, callback
        var command = `print(list(${varName}.${property}))`;
        this.kernelExecute(command, function(result) {
            var jsonVars = result.replace(/'/gi, `"`);
            var varList = JSON.parse(jsonVars);

            var optVar = '<option value=""></option>';
            varList.forEach(obj => {
                optVar += `<option value="${obj}">${obj}</option>`;
            });

            $(that.wrapSelector(selectId)).html(optVar);

            // replace board with now status of board option
            that.replaceBoard();
        });      
    };

    /**
     * TEST: 선택한 변수 유형에 따라 가능한 api list 보여주기
     */
    VariablePackage.prototype.loadApiList = function() {
        var that = this;

        // get selected variable & data type
        var returnType = $(this.wrapSelector('#vp_returnType')).val();
        
        // init
        $(this.wrapSelector('#vp_varApiList')).html('<ul class="vp-var-api-list"></ul>');
        $(this.wrapSelector('#vp_varApiSearch')).val('');
        $(this.wrapSelector('#vp_varApiFuncId')).val('');
        $(this.wrapSelector('#vp_varApiSearch')).autocomplete('option', 'source', []);

        // api list
        var apiListTag = '';
        this.apiList[returnType] != undefined && this.apiList[returnType].forEach(obj => {
            apiListTag += `<li class="vp-var-api-item" data-item-code="${obj.code}" data-item-id="${obj.funcID == undefined? "": obj.funcID}">${obj.name}</li>`;
        });
        $(this.wrapSelector('#vp_varApiList ul')).html(apiListTag);

        // search list
        var source = this.apiList[returnType];
        $(this.wrapSelector('#vp_varApiSearch')).autocomplete('option', 
        'source', function (request, response) {
            var data = request.term;
            var filteredSource = source.filter(x => (x.name.indexOf(data) >= 0));
            response($.map(filteredSource, function (item) {
                return {
                    id: item.funcID,
                    label: item.name,
                    value: item.code
                }
            }))
        });

        // api list selection
        $(this.wrapSelector('#vp_varApiList ul li')).click(function() {
            var apiCode = $(this).attr('data-item-code');
            var apiFuncId = $(this).attr('data-item-id');

            $(that.wrapSelector('#vp_varApiSearch')).val(apiCode);
            $(that.wrapSelector('#vp_varApiFuncId')).val(apiFuncId);

            that.replaceBoard();
        });
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    VariablePackage.prototype.generateCode = function(addCell, exec) {
        if (!this.optionValidation()) return;
        
        var sbCode = new sb.StringBuilder();
        
        // 생성된 것 표시
        sbCode.appendLine(`# Auto-Generated by VisualPython`);

        // TODO: 변수 내용 조회
        var boardCode = vpBoard.getCode();
        if (boardCode == undefined) return "BREAK_RUN"; // 코드 생성 중 오류 발생
        
        sbCode.appendFormat('{0}', boardCode);

        if (addCell) this.cellExecute(sbCode.toString(), exec);

        return sbCode.toString();
    }

    return {
        initOption: initOption
    };
});