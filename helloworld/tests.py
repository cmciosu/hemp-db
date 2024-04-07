## Django Testing
from django.test import TestCase
## Models
from .models import *

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(category="testCategory")
        Category.objects.create(category="anotherTestCategory")

    def test_categories_are_created(self):
        c1 = Category.objects.get(category="testCategory")
        c2 = Category.objects.get(category="anotherTestCategory")
        self.assertTrue(c1)
        self.assertTrue(c2)

class SolutionTestCase(TestCase):
    def setUp(self):
        Solution.objects.create(solution="testSolution")
        Solution.objects.create(solution="anotherTestSolution")

    def test_solutions_are_created(self):
        c1 = Solution.objects.get(solution="testSolution")
        c2 = Solution.objects.get(solution="anotherTestSolution")
        self.assertTrue(c1)
        self.assertTrue(c2)

class StakeholderGroupsTestCase(TestCase):
    def setUp(self):
        stakeholderGroups.objects.create(stakeholderGroup="testGroup")
        stakeholderGroups.objects.create(stakeholderGroup="anotherTestGroup")

    def test_groups_are_created(self):
        c1 = stakeholderGroups.objects.get(stakeholderGroup="testGroup")
        c2 = stakeholderGroups.objects.get(stakeholderGroup="anotherTestGroup")
        self.assertTrue(c1)
        self.assertTrue(c2)

class StagesTestCase(TestCase):
    def setUp(self):
        Stage.objects.create(stage="testStage")
        Stage.objects.create(stage="anotherTestStage")

    def test_stages_are_created(self):
        c1 = Stage.objects.get(stage="testStage")
        c2 = Stage.objects.get(stage="anotherTestStage")
        self.assertTrue(c1)
        self.assertTrue(c2)

class ProductGroupTestCase(TestCase):
    def setUp(self):
        ProductGroup.objects.create(productGroup="testProductGroup")
        ProductGroup.objects.create(productGroup="anotherTestProductGroup")

    def test_product_groups_are_created(self):
        c1 = ProductGroup.objects.get(productGroup="testProductGroup")
        c2 = ProductGroup.objects.get(productGroup="anotherTestProductGroup")
        self.assertTrue(c1)
        self.assertTrue(c2)

class ProcessingFocusTestCase(TestCase):
    def setUp(self):
        ProcessingFocus.objects.create(processingFocus="testProcessingFocus")
        ProcessingFocus.objects.create(processingFocus="anotherTestProcessingFocus")

    def test_processing_focus_are_created(self):
        c1 = ProcessingFocus.objects.get(processingFocus="testProcessingFocus")
        c2 = ProcessingFocus.objects.get(processingFocus="anotherTestProcessingFocus")
        self.assertTrue(c1)
        self.assertTrue(c2)

class ExtractionTypesTestCase(TestCase):
    def setUp(self):
        ExtractionType.objects.create(extractionType="testExtractionType")
        ExtractionType.objects.create(extractionType="anotherTestExtractionType")

    def test_extraction_types_are_created(self):
        c1 = ExtractionType.objects.get(extractionType="testExtractionType")
        c2 = ExtractionType.objects.get(extractionType="anotherTestExtractionType")
        self.assertTrue(c1)
        self.assertTrue(c2)

class CompanyTestCase(TestCase):
    def setUp(self):
        Solution.objects.create(solution="testSolution")

        Company.objects.create(
            Name="test",
            Industry="test",
            Status="test",
            Info="test",
            Headquarters="test",
            Sales="test",
            Product="test",
            City="test",
            State="test",
            Country="test",
            Solutions=Solution.objects.get(solution="testSolution"),
            Website="test",
            Category=Category.objects.create(category="testCategory"),
            stakeholderGroup=stakeholderGroups.objects.create(stakeholderGroup="testStakeholderGroup"),
            Stage=Stage.objects.create(stage="testStage"),
            productGroup=ProductGroup.objects.create(productGroup="testProductGroup"),
            Products="test",
            sasContact="test",
            Description="test",
            pubPriv="test",
            Ticker="test",
            Naics="test",
            Phone="test",
            Email="test",
            Stakeholder="test",
            Principal="test",
            Founded="test",
            Employees="test",
            parentCompany="test",
            onMarket="test",
            productName="test",
            SKU="test",
            Notes="test",
            salesRev="test",
            processingFocus=ProcessingFocus.objects.create(processingFocus="testProcessingFocus"),
            facilitySize="test",
            biomassCap="test",
            extractionType=ExtractionType.objects.create(extractionType="testExtractionType"),
            GMP="test",
            news="test",
            reviews="test",
        )
        Company.objects.create(
            Name="test2",
            Industry="test",
            Status="test",
            Info="test",
            Headquarters="test",
            Sales="test",
            Product="test",
            City="test",
            State="test",
            Country="test",
            Solutions=Solution.objects.get(solution="testSolution"),
            Website="test",
            Category=Category.objects.create(category="testCategory"),
            stakeholderGroup=stakeholderGroups.objects.create(stakeholderGroup="testStakeholderGroup"),
            Stage=Stage.objects.create(stage="testStage"),
            productGroup=ProductGroup.objects.create(productGroup="testProductGroup"),
            Products="test",
            sasContact="test",
            Description="test",
            pubPriv="test",
            Ticker="test",
            Naics="test",
            Phone="test",
            Email="test",
            Stakeholder="test",
            Principal="test",
            Founded="test",
            Employees="test",
            parentCompany="test",
            onMarket="test",
            productName="test",
            SKU="test",
            Notes="test",
            salesRev="test",
            processingFocus=ProcessingFocus.objects.create(processingFocus="testProcessingFocus"),
            facilitySize="test",
            biomassCap="test",
            extractionType=ExtractionType.objects.create(extractionType="testExtractionType"),
            GMP="test",
            news="test",
            reviews="test",
        )

    def test_companies_are_created(self):
        c1 = Company.objects.get(Name="test")
        c2 = Company.objects.get(Name="test2")
        self.assertTrue(c1)
        self.assertTrue(c2)

    def test_company_persists_on_delete(self):
        sol = Solution.objects.get(solution="testSolution")
        c1 = Company.objects.get(Name="test")
        sol.delete()
        self.assertTrue(c1)

