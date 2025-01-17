from django.db import models
from django.contrib.auth import get_user_model

# ใช้ CustomUser สำหรับผู้ใช้
User = get_user_model()





class WasteImage(models.Model):
    WASTE_TYPE_CHOICES = [
        ('plastic', 'พลาสติก'),
        ('paper', 'กระดาษ'),
        ('metal', 'โลหะ'),
        ('glass', 'แก้ว'),
        ('e_waste', 'e-waste'),
        ('steel', 'เหล็ก'),
        ('others', 'อื่นๆ'),
    ]

    CATEGORY_CHOICES = [
        ('recyclable', 'สามารถรีไซเคิลได้'),
        ('non_recyclable', 'ไม่สามารถรีไซเคิลได้'),
        ('hazardous', 'ของเสียอันตราย'),
        ('compostable', 'สามารถย่อยสลายได้'),
    ]

    image = models.ImageField(
        upload_to='waste_images/',
        blank=True,
        null=True,
        verbose_name='รูปภาพขยะ'
    )
    waste_type = models.CharField(
        max_length=50,
        choices=WASTE_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='ประเภทขยะ'
    )
    subtype = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='หมวดหมู่ย่อย'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        verbose_name='หมวดหมู่'
    )
    separation_method = models.TextField(
        blank=True,
        null=True,
        verbose_name='วิธีการแยกขยะ'
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='ผู้เพิ่มข้อมูล'
    )
    
    waste_item = models.ForeignKey(
    'WasteItem',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name='รายการขยะที่เชื่อมโยง'
)




    # ฟิลด์สำหรับกดไลค์ "แยกถูก" และ "แยกผิด"
    correct_votes = models.ManyToManyField(
        User,
        related_name='correct_waste_images',
        blank=True,
        verbose_name='แยกถูก'
    )
    incorrect_votes = models.ManyToManyField(
        User,
        related_name='incorrect_waste_images',
        blank=True,
        verbose_name='แยกผิด'
    )

    def total_correct_votes(self):
        return self.correct_votes.count()

    def total_incorrect_votes(self):
        return self.incorrect_votes.count()

    def __str__(self):
        return f"{self.waste_type} - {self.category}"



class WasteItem(models.Model):
    barcode = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='เลขบาร์โค้ด'
    )
    brand_name = models.CharField(
        max_length=255,
        verbose_name='ชื่อยี่ห้อ',
        default='Unknown'
    )
    product_name = models.CharField(
        max_length=255,
        verbose_name='ชื่อสินค้า / รุ่น / ประเภท'
    )
    product_image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        verbose_name='ภาพผลิตภัณฑ์'
    )
    images = models.ManyToManyField(
        'WasteImage',
        blank=True,
        verbose_name='รูปภาพที่เกี่ยวข้อง'
    )
    created_by = models.ForeignKey(
        User,  # ใช้ CustomUser
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='ผู้สร้างผลิตภัณฑ์'
    )

    def __str__(self):
        return f"{self.product_name} ({self.barcode})"




