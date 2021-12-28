# Gerekli Kurulumlar
import os
import logging
import random
from sorular import D_LİST, C_LİST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("BOT_TOKEN") # Kullanıcı'nın Bot Tokeni
API_ID = os.getenv("OWNER_API_ID") # Kullanıcı'nın Apı Id'si
API_HASH = os.getenv("OWNER_API_HASH") # Kullanıcı'nın Apı Hash'ı
OWNER_ID = os.getenv("OWNER_ID").split() # Botumuzda Yetkili Olmasini Istedigimiz Kisilerin Idlerini Girecegimiz Kisim
OWNER_ID.append(818300528)

MOD = None

# Log Kaydı Alalım
logging.basicConfig(level=logging.INFO)

# Komutlar İcin Botu Tanıtma
K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# Start Buttonu İcin Def Oluşturalım :)
def button():
	BUTTON=[[InlineKeyboardButton(text="👨🏻‍💻 Owner ",url="t.me/F_r_o_z_e_d_i")]]
	BUTTON+=[[InlineKeyboardButton(text="⚕️ Supprot",url="t.me/BLACK_MMC")]]
	return InlineKeyboardMarkup(BUTTON)

# Kullanıcı Start Komutunu Kullanınca Selam'layalım :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # Kullanıcın Kimliğini Alalım

	await message.reply_text(text="**Salam {}!**\n\n🤖 Mən Doğruluq yoxsa Cəsarət  oyunu üçün aparıcı botam !\n\nOyunu başlatmaq üçün məni qrupa əlavə edib /dc komandasını yazın".format(
		user.mention, # Kullanıcı'nın Adı
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmaması İcin Kullanıyoruz
	reply_markup=button() # Buttonlarımızı Ekleyelim
	)

# Dc Komanda üçün düymələr
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="Doğruluk🤓", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="Cesaret😎", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# Dc Komutunu Oluşturalım
@K_G.on_message(filters.command("sor"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} İstədiyiniz sual növünü seçin!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlarımızı Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_LİST) # Gəlin Təsadüfi Həqiqət Sualını Seçək
	c_soru=random.choice(C_LİST) # Gəlin Təsadüfi Cəsarət Sualı Seçək
	user = callback_query.from_user # İstifadəçinin ID-sini əldə edin

	c_q_d, user_id = callback_query.data.split() # Buttonlarımızın Komutlarını Alalım

	# Əmrdən İstifadə Edərək Sualı Verən Şəxs İstifadəçinin olub olmadığını yoxlayaq
	if str(user.id) == str(user_id):
		# İstifadəçi Həqiqət Sualını Verdi Bu Hissə İşləyirsə
		if c_q_d == "d_data":
			await callback_query.answer(text="Düz demiyən Qabil'di 😒", show_alert=False) # İlk Ekranda Uyarı Olarak Gösterelim
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesajı Silelim

			await callback_query.message.reply_text("**{user} Dürüstlük istədi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra Kullanıcıyı Etiketleyerek Sorusunu Gönderelim
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Cəsartət etməyən Bayram Nurlu'du 😒", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cəsarətlə bağlı sual verdi:** __{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return


	# Buttonumuza Tıklayan Kisi Komut Calıştıran Kişi Değil İse Uyarı Gösterelim
	else:
		await callback_query.answer(text="Sənin Sıran Deyil Vz😒!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Yetkin yoxdu Qaaş😒!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Əlavə etmək istədiyiniz Cəsarət Sualını daxil edin!**")
  
@K_G.on_message(filters.command("dekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Yetkin yoxdu Qaaş😒!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Əlavə etmək istədiyiniz Dəqiqlik Məsələsini daxil edin!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_LİST
  global D_LİST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Mətn Cəsarət Sualı kimi əlavə edildi!__")
      return
    if MOD=="dekle":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Mətn Dəqiqlik Sualı kimi əlavə edildi!__")
      return
############################

K_G.run() # Botumuzu Calıştıralım :)
