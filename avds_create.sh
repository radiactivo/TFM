#################
# Avds creation #
#################

echo 'no' | $android/tools/bin/avdmanager create avd -p $tfm/avds/nougat_7.1 -n nougat_7.1 -k "system-images;android-25;google_apis;x86" --force
echo 'no' | $android/tools/bin/avdmanager create avd -p $tfm/avds/nougat_7.0 -n nougat_7.0 -k "system-images;android-24;google_apis;x86" --force
echo 'no' | $android/tools/bin/avdmanager create avd -p $tfm/avds/marshmallow -n marshmallow -k "system-images;android-23;google_apis;x86" --force
echo 'no' | $android/tools/bin/avdmanager create avd -p $tfm/avds/lollipop -n lollipop -k "system-images;android-21;google_apis;x86" --force