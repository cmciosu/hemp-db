from django.test import TestCase
from .models import Company
from .models import PendingCompany
from .models import Category
from .models import Solution
from .models import stakeholderGroups
from .models import Stage
from .models import ProductGroup
from .models import Grower
from .models import Industry
from .models import Status

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
        stakeholderGroups.objects.create(stakeholderGroup="testGroup", category=1)
        stakeholderGroups.objects.create(stakeholderGroup="anotherTestGroup", category=1)

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

class GrowerTestCase(TestCase):
    def setUp(self):
        Grower.objects.create(grower="testGrower")
        Grower.objects.create(grower="anotherTestGrower")

    def test_growers_are_created(self):
        c1 = Grower.objects.get(grower="testGrower")
        c2 = Grower.objects.get(grower="anotherTestGrower")
        self.assertTrue(c1)
        self.assertTrue(c2)

class StatusTestCase(TestCase):
    def setUp(self):
        Status.objects.create(status="testStatus")
        Status.objects.create(status="anotherTestStatus")

    def test_status_are_created(self):
        c1 = Status.objects.get(status="testStatus")
        c2 = Status.objects.get(status="anotherTestStatus")
        self.assertTrue(c1)
        self.assertTrue(c2)

class IndustryTestCase(TestCase):
    def setUp(self):
        Industry.objects.create(industry="testIndustry")
        Industry.objects.create(industry="anotherTestIndustry")

    def test_industries_are_created(self):
        c1 = Industry.objects.get(industry="testIndustry")
        c2 = Industry.objects.get(industry="anotherTestIndustry")
        self.assertTrue(c1)
        self.assertTrue(c2)

class CompanyTestCase(TestCase):
    def setUp(self):
        c1 = Company.objects.create(
            SrcKey="OSU",
            Name="test",
            Industry=Industry.objects.create(industry="testIndustry"),
            Status=Status.objects.create(status="testStatus"),
            Headquarters="test",
            Sales="test",
            Product="test",
            Grower=Grower.objects.create(grower="testGrower"),
            City="test",
            State="test",
            Country="test",
            Address="123 Way",
            Website="test",
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
            processingFocus="test",
            facilitySize="test",
            biomassCap="test",
            extractionType="test",
            GMP="test",
            news="test",
            reviews="test",
        )
        c1.Solutions.add(Solution.objects.create(solution="testSolution"))
        c1.Category.add(Category.objects.create(category="testCategory"))
        c1.stakeholderGroup.add(stakeholderGroups.objects.create(stakeholderGroup="testStakeholderGroup", category=1))
        c1.Stage.add(Stage.objects.create(stage="testStage"))
        c1.productGroup.add(ProductGroup.objects.create(productGroup="testProductGroup"))
        
        c2 = Company.objects.create(
            SrcKey="OSU",
            Name="test2",
            Industry=Industry.objects.create(industry="testIndustry"),
            Status=Status.objects.create(status="testStatus"),
            Headquarters="test",
            Sales="test",
            Product="test",
            Grower=Grower.objects.create(grower="testGrower"),
            City="test",
            State="test",
            Country="test",
            Address="123 Way",
            Website="test",
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
            processingFocus="test",
            facilitySize="test",
            biomassCap="test",
            extractionType="test",
            GMP="test",
            news="test",
            reviews="test",
        )
        c2.Solutions.add(Solution.objects.create(solution="testSolution"))
        c2.Category.add(Category.objects.create(category="testCategory"))
        c2.stakeholderGroup.add(stakeholderGroups.objects.create(stakeholderGroup="testStakeholderGroup", category=1))
        c2.Stage.add(Stage.objects.create(stage="testStage"))
        c2.productGroup.add(ProductGroup.objects.create(productGroup="testProductGroup"))

    def test_companies_are_created(self):
        c1 = Company.objects.get(Name="test")
        c2 = Company.objects.get(Name="test2")
        self.assertTrue(c1)
        self.assertTrue(c2)

class PendingCompanyTestCase(TestCase):
    def setUp(self):
        c1 = PendingCompany.objects.create(
            SrcKey="OSU",
            Name="test",
            Industry=Industry.objects.create(industry="testIndustry"),
            Status=Status.objects.create(status="testStatus"),
            Headquarters="test",
            Sales="test",
            Product="test",
            Grower=Grower.objects.create(grower="testGrower"),
            City="test",
            State="test",
            Country="test",
            Address="123 Way",
            Website="test",
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
            processingFocus="test",
            facilitySize="test",
            biomassCap="test",
            extractionType="test",
            GMP="test",
            news="test",
            reviews="test",
        )
        c1.Solutions.add(Solution.objects.create(solution="testSolution"))
        c1.Category.add(Category.objects.create(category="testCategory"))
        c1.stakeholderGroup.add(stakeholderGroups.objects.create(stakeholderGroup="testStakeholderGroup", category=1))
        c1.Stage.add(Stage.objects.create(stage="testStage"))
        c1.productGroup.add(ProductGroup.objects.create(productGroup="testProductGroup"))
        
        c2 = PendingCompany.objects.create(
            SrcKey="OSU",
            Name="test2",
            Industry=Industry.objects.create(industry="testIndustry"),
            Status=Status.objects.create(status="testStatus"),
            Headquarters="test",
            Sales="test",
            Product="test",
            Grower=Grower.objects.create(grower="testGrower"),
            City="test",
            State="test",
            Country="test",
            Address="123 Way",
            Website="test",
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
            processingFocus="test",
            facilitySize="test",
            biomassCap="test",
            extractionType="test",
            GMP="test",
            news="test",
            reviews="test",
        )
        c2.Solutions.add(Solution.objects.create(solution="testSolution"))
        c2.Category.add(Category.objects.create(category="testCategory"))
        c2.stakeholderGroup.add(stakeholderGroups.objects.create(stakeholderGroup="testStakeholderGroup", category=1))
        c2.Stage.add(Stage.objects.create(stage="testStage"))
        c2.productGroup.add(ProductGroup.objects.create(productGroup="testProductGroup"))

    def test_companies_are_created(self):
        c1 = PendingCompany.objects.get(Name="test")
        c2 = PendingCompany.objects.get(Name="test2")
        self.assertTrue(c1)
        self.assertTrue(c2)

