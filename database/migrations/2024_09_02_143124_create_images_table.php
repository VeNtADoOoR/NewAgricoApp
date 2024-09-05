<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateImagesTable extends Migration
{
    public function up()
    {
        Schema::create('images', function (Blueprint $table) {
            $table->id();
            $table->string('original_filename');
            $table->string('path');
            $table->unsignedBigInteger('user_id'); // Assuming images are associated with a user
            $table->boolean('is_processed')->default(false);
            $table->string('correction_status')->nullable(); // E.g., 'radiometric', 'atmospheric', etc.
            $table->json('indices')->nullable(); // Store vegetation indices as JSON
            $table->timestamps();

            // Foreign key constraint
            $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
        });
    }

    public function down()
    {
        Schema::dropIfExists('images');
    }
}
