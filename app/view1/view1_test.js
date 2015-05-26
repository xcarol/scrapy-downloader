'use strict';

describe('myApp.view1 module', function () {

    beforeEach(module('myApp.view1'));

    describe('view1 controller', function () {
        var scope = {};
        var ctrl;
        var $httpBackend;

        beforeEach(inject(function (_$httpBackend_, $rootScope, $controller) {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('../series.json').respond([{
                "name": "American Horror Story",
                "season": 4,
                "chapter": 13,
                "enabled": "True",
                "url": "http://www.divxtotal.com/series/american-horror-story-453/",
                "xpath": "//td[@class=\"capitulodescarga\"]/a",
                "xpath_link": "@href",
                "xpath_title": "",
                "link_prefix": "http://www.divxtotal.com",
                "link_mask": "Story.#1x#2.HDTV",
                "file_mask": "American.Horror.Story.#1x#2",
                "title_mask": ""
            }]);

            scope = $rootScope.$new();
            ctrl = $controller('View1Ctrl', {$scope: scope});
        }));

        it('should ....', inject(function ($controller) {
            var view1Ctrl = $controller('View1Ctrl', {$scope: scope});
            expect(view1Ctrl).toBeDefined();
        }));

        it('should create a serie model with all fields ...', inject(function(){
            expect(scope.series).toBeUndefined();
            $httpBackend.flush();
            expect(scope.series.length).toBeGreaterThan(0);

            var serie = scope.series[0];

            expect(serie.chapter).toBeDefined();
            expect(serie.xpath).toBeDefined();
            expect(serie.name).toBeDefined();
            expect(serie.url).toBeDefined();
            expect(serie.season).toBeDefined();
            expect(serie.xpath_link).toBeDefined();
            expect(serie.enabled).toBeDefined();
            expect(serie.link_prefix).toBeDefined();
            expect(serie.file_mask).toBeDefined();
            expect(serie.link_mask).toBeDefined();
            expect(serie.xpath_title).toBeDefined();
            expect(serie.title_mask).toBeDefined();
        }));
    });
});